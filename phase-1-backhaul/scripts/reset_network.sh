#!/bin/bash
# reset_network.sh - Removes all tc rules, restoring the network to normal

echo "[INFO] Removing all network impairment rules..."
sudo tc qdisc del dev enp0s3 root 2>/dev/null || true
echo "[INFO] Network reset to normal state."

