#!/usr/bin/env python3
import subprocess
import time
import logging

# Configure logging to see informative messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
PING_TARGET = "8.8.8.8"
LATENCY_THRESHOLD_MS = 150 # ms
CHECK_INTERVAL = 10 # seconds

def run_command(cmd):
    """Execute a shell command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output = True, text=True)
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

def enable_qos():
    """Apply QoS rules to prioritize ICMP (ping) traffic over other traffic."""
    logger.info("Enabling QoS remediation...")
    # 1 - Flush any existing rules
    run_command("sudo tc qdisc del dev enp0s3 root 2>/dev/null")
    # 2 - Create a Priority Queueing discipline with 3 bands
    run_command("sudo tc qdisc add dev enp0s3 root handle 1: prio bands 3")
    # 3 - Create a filter to send ICMP (protocol 1) to the high-priority band (1:1)
    run_command("sudo tc filter add dev enp0s3 protocol ip parent 1:0 prio 1 u32 match ip protocol 1 0xff flowid 1:1")
    # 4 - Apply the original impairment (delay, loss, rate limit) only to lower priority bands (1:2 and 1:3)
    run_command("sudo tc qdisc add dev enp0s3 parent 1:2 handle 30: netem delay 100ms loss 2% rate 1mbit")
    run_command("sudo tc qdisc add dev enp0s3 parent 1:3 handle 40: netem delay 100ms loss 2% rate 1mbit")
    logger.info("QoS rules applied. ICMP traffic is now prioritized.")

def main():
    logger.info("Starting network monitor...")
    logger.info(f"Configuration: Threshold={LATENCY_THRESHOLD_MS}ms, Check-Interval={CHECK_INTERVAL}s")

    try:
        while True:
            latency=measure_latency()
            if latency is None:
             logger.error("Failed to measure latency. Check network connectivity.")
            elif latency > LATENCY_THRESHOLD_MS:
             logger.warning(f"Congestion detected! Latency: {latency}ms > {LATENCY_THRESHOLD_MS}ms threshold")
             enable_qos()
             logger.info("Remediation complete. Monitor will now exit. Run reset_network.sh to return to normal.")
             break # Exit after remediation for a clean demo
            else :
             logger.info(f"Network normal. Latency: {latency}ms")

            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
      logger.info("Monitor stopped by user.")

if __name__ == "__main__":
   main()

