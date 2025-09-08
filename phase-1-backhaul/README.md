# Phase 1: 5G Backhaul & QoS Simulation

## Objective
Simulate and analyze network congestion on a shared backhaul link and implement a Quality of Service (QoS) policy to prioritize critical traffic.

## Theory
In a 5G network, the backhaul connects the radio unit to the core network. Congestion here causes latency and packet loss. QoS mechanisms like priority queuing are used to ensure performance for sensitive applications like voice and video.

## 📁 Structure
```
phase-1-backhaul/
├── scripts/
│   ├── impair_network.sh     # Applies 'tc' rules to create congestion
│   ├── enable_qos.sh         # Applies 'tc' rules to implement QoS
│   └── monitor.py            # Python script to detect congestion
├── docs/
│   └── captures/             # Wireshark PCAPs and screenshots
└── docker-compose.yml        # Defines traffic-generator containers
```

## 🚀 How to Run

1.  **Start the traffic generators:**
    ```bash
    docker-compose up -d
    ```
2.  **Apply network impairment (simulate congestion):**
    ```bash
    sudo bash scripts/impair_network.sh
    ```
3.  **Run the monitoring script to auto-detect and remediate:**
    ```bash
    python3 scripts/monitor.py
    ```
4.  **Validate:** Use `ping 8.8.8.8` and `iperf3 -c your-vm-ip` to observe performance before, during, and after remediation.

## 🔍 Validation
Successful implementation will be shown by:
1.  A significant increase in latency and drop in throughput after running `impair_network.sh`.
2.  The `monitor.py` script logging "Congestion detected".
3.  Latency for ping traffic recovering after the script runs `enable_qos.sh`, while bulk throughput remains limited.
