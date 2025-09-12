# Phase 1: 5G Backhaul & QoS Simulation

## Objective
Simulate and analyze network congestion on a shared backhaul link and implement a Quality of Service (QoS) policy to prioritize critical traffic.

---

## 📂 Repository Structure

```
phase-1-backhaul/
├── scripts/
│   ├── monitorinit.py           # Initial congestion detection script
│   ├── monitor_progressive.py   # Progressive congestion simulation
│   ├── monitor.py               # Final script with jitter and rate limiting
├── docs/
│   ├── iperf3-before.pdf
│   ├── iperf3-after.pdf
│   ├── terminal-monitorinit-output.png
│   ├── terminal-monitor-progressive-output.png
│   ├── wireshark-monitorinit.pdf
│   ├── wireshark-monitor-progressive.pdf
│   ├── wireshark-monitor-final.pdf
│   ├── PHASE-1-EXECUTION-NOTES.md
└── README.md
```

---

## 🚀 How to Run

1. **Start Traffic Generators**:
   ```bash
   docker-compose up -d
   ```

2. **Apply Network Impairment**:
   ```bash
   sudo bash scripts/impair_network.sh
   ```

3. **Run the Monitoring Script**:
   Choose the script based on the stage:
   - **Basic Detection**: `python3 scripts/monitorinit.py`
   - **Progressive Simulation**: `python3 scripts/monitor_progressive.py`
   - **Final Simulation**: `python3 scripts/monitor.py`

4. **Validate the Network**:
   - Use `iperf3 -c <target-ip>` to measure throughput.
   - Use `ping 8.8.8.8` to measure latency.

---

## 📊 Analysis
For detailed execution notes and Wireshark/iperf3 results, refer to the [Execution Notes](./docs/PHASE-1-EXECUTION-NOTES.md).