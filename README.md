# 5g-network-sim-ubuntu-server
An Ubuntu Server VM-based simulation of a 5G network, featuring backhaul congestion as the first phase, network slicing as the second phase, and a file-based core as the third phase.

## 🚧 Project Phases

This project is built incrementally. Each phase depends on the previous one.

| Phase | Name | Description | Status |
| :--- | :--- | :--- | :--- |
| 1 | [Backhaul & QoS Simulation](./phase-1-backhaul/) | Simulates and mitigates network congestion. | **Completed** |
| 2 | [Network Slicing](./phase-2-slicing/) | Implements logical network isolation. | Planned |
| 3 | [File-Based 5G Core](./phase-3-core/) | Simulates AMF, SMF, and UPF signaling. | Planned |

## 🛠️ Tech Stack

* **Platform:** Ubuntu Linux
* **Virtualization:** Docker, Docker Compose
* **Networking:** `tc` (Traffic Control), `iptables`, Linux Network Namespaces, `veth`
* **Scripting:** Bash, Python
* **Monitoring:** Wireshark, `ping`, `iperf3`, `iftop`

## 📂 Repository Structure

```
5g-network-sim-ubuntu-server/
├── phase-1-backhaul/
│   ├── scripts/
│   │   ├── monitorinit.py
│   │   ├── monitor_progressive.py
│   │   ├── monitor.py
│   ├── docs/
│   │   ├── BackhaulOut/
│   │   │   ├── before-vs-after-impair-network.sh.png
│   │   │   ├── monitor-progressive-wireshark.pdf
│   │   │   ├── monitorinit.py_output.png
│   │   │   ├── monitor.py_output.png
│   │   │   ├── monitor-init-wireshark.pdf
│   │   │   ├── monitor-wireshark.pdf
│   │   │   ├── monitor_progressive.py_output.png
│   ├── README.md
│   ├── PHASE-1-EXECUTION-NOTES.md
├── LICENSE
└── README.md
```

## 📝 Getting Started

1. **Install Prerequisites**:
   ```bash
   sudo apt update && sudo apt install -y docker.io python3-pip iperf3
   ```

2. **Navigate to the Desired Phase**:
   ```bash
   cd phase-1-backhaul
   ```

3. **Follow Phase-Specific Instructions**:
   Refer to the `README.md` in each phase folder.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
