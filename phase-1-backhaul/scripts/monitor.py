#!/usr/bin/env python3
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
PING_TARGET = "8.8.8.8"
LATENCY_THRESHOLD_MS = 150  # ms
CHECK_INTERVAL = 7  # seconds

# More realistic impairment progression for 5G backhaul congestion
IMPAIRMENT_STEPS = [
    {"delay": "10ms", "jitter": "2ms",  "loss": "0.1%", "rate": "45mbit"},  # Light congestion
    {"delay": "50ms", "jitter": "10ms", "loss": "1%",   "rate": "30mbit"},  # Moderate congestion
    {"delay": "100ms", "jitter": "20ms", "loss": "2%",  "rate": "20mbit"},  # Heavy congestion
    {"delay": "200ms", "jitter": "40ms", "loss": "5%",  "rate": "10mbit"},  # Severe congestion
]

def run_command(cmd):
    """Execute a shell command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.stderr}")
        return None

def measure_latency():
    """Measure average ping latency to target. Returns latency in ms or None."""
    cmd = f"ping -c 4 {PING_TARGET} | tail -1 | awk -F '/' '{{print $5}}'"
    output = run_command(cmd)
    try:
        return float(output) if output else None
    except ValueError:
        logger.warning(f"Could not parse ping output: {output}")
        return None

def apply_impairment(step):
    """Apply network impairment to simulate realistic 5G backhaul congestion."""
    delay = step["delay"]
    jitter = step["jitter"]
    loss = step["loss"]
    rate = step["rate"]
    logger.info(f"Applying impairment: delay={delay} ±{jitter}, loss={loss}, rate={rate}")
    run_command("sudo tc qdisc del dev enp0s3 root 2>/dev/null")
    run_command(f"sudo tc qdisc add dev enp0s3 root netem delay {delay} {jitter} "
                f"distribution normal loss {loss} rate {rate}")

def enable_qos():
    """Apply QoS rules to prioritize ICMP (ping) traffic over other traffic."""
    logger.info("Enabling QoS remediation...")
    # 1 - Flush any existing rules
    run_command("sudo tc qdisc del dev enp0s3 root 2>/dev/null")
    # 2 - Create a Priority Queueing discipline with 3 bands
    run_command("sudo tc qdisc add dev enp0s3 root handle 1: prio bands 3")
    # 3 - Create a filter to send ICMP (protocol 1) to the high-priority band (1:1)
    run_command("sudo tc filter add dev enp0s3 protocol ip parent 1:0 prio 1 u32 match ip protocol 1 0xff flowid 1:1")
    # 4 - Apply improved remediation with better parameters for lower priority bands
    run_command("sudo tc qdisc add dev enp0s3 parent 1:2 handle 30: netem delay 100ms 20ms "
                "distribution normal loss 2% rate 10mbit")
    run_command("sudo tc qdisc add dev enp0s3 parent 1:3 handle 40: netem delay 150ms 30ms "
                "distribution normal loss 3% rate 5mbit")
    logger.info("QoS rules applied. ICMP traffic is now prioritized.")

def main():
    logger.info("Starting 5G backhaul congestion simulator...")
    logger.info(f"Configuration: Threshold={LATENCY_THRESHOLD_MS}ms, Check-Interval={CHECK_INTERVAL}s")

    try:
        # Apply progressive impairments to simulate worsening congestion
        for i, step in enumerate(IMPAIRMENT_STEPS):
            logger.info(f"Simulating congestion level {i+1}/{len(IMPAIRMENT_STEPS)}")
            apply_impairment(step)
            time.sleep(CHECK_INTERVAL)  # Let impairment settle
            
            latency = measure_latency()
            if latency is None:
                logger.error("Failed to measure latency. Check network connectivity.")
                continue
            elif latency > LATENCY_THRESHOLD_MS:
                logger.warning(f"Congestion detected! Latency: {latency}ms > {LATENCY_THRESHOLD_MS}ms threshold")
                enable_qos()
                
                # Measure post-remediation latency
                time.sleep(3)
                new_latency = measure_latency()
                if new_latency is not None:
                    logger.info(f"Post-remediation latency: {new_latency}ms")
                
                logger.info("Remediation complete. Monitor will now exit. Run reset_network.sh to return to normal.")
                break  # Exit after remediation for a clean demo
            else:
                logger.info(f"Network condition level {i+1}: {latency}ms latency (threshold: {LATENCY_THRESHOLD_MS}ms)")
    except KeyboardInterrupt:
        logger.info("Monitor stopped by user.")
        # Clean up on exit
        run_command("sudo tc qdisc del dev enp0s3 root 2>/dev/null")

if __name__ == "__main__":
    main()
