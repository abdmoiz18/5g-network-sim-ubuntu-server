# 5g-network-sim-ubuntu-server
An Ubuntu Server VM-based simulation of a 5G network, featuring backhaul congestion as the first phase, network slicing as the second phase, and a file-based core as the third phase
# 5G Network Simulator

A Linux-based software-defined project simulating key 5G concepts: **backhaul congestion**, **network slicing**, and **core network signaling**, built with Docker, Linux `tc`, network namespaces, and a file-based control plane.

## 🚧 Project Phases

This project is built incrementally. Each phase depends on the previous one.

| Phase | Name | Description | Status |
| :--- | :--- | :--- | :--- |
| 1 | [Backhaul & QoS Simulation](./phase-1-backhaul/) | Simulates and mitigates network congestion. | **Planned** |
| 2 | [Network Slicing](./phase-2-slicing/) | Implements logical network isolation. | Planned |
| 3 | [File-Based 5G Core](./phase-3-core/) | Simulates AMF, SMF, and UPF signaling. | Planned |

## 🛠️ Tech Stack

*   **Platform:** Ubuntu Linux
*   **Virtualization:** Docker, Docker Compose
*   **Networking:** `tc` (Traffic Control), `iptables`, Linux Network Namespaces, `veth`
*   **Scripting:** Bash, Python
*   **Monitoring:** Wireshark, `ping`, `iperf3`, `iftop`

## 📚 Getting Started

1.  **Prerequisites:** Ensure you have Docker and `pip3` installed.
    ```bash
    sudo apt update && sudo apt install -y docker.io python3-pip iperf3
    ```
2.  Navigate to the phase you want to run, e.g., `cd phase-1-backhaul`.
3.  Follow the phase-specific instructions in its `README.md`.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
