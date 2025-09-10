#!/bin/bash
# impair_network.sh - Simulates 5G backhaul congestion (delay, loss, bandwidth limit)

echo "[INFO] Applying network impairment (congestion simulation)..."

# Check if impairment is already applied to avoid errors
if sudo tc qdisc show dev enp0s3 | grep -q "netem"; then
    echo "[WARN] Network impairment rules already exist. Resetting first."
    sudo tc qdisc del dev enp0s3 root 2>/dev/null
fi

# Apply impairment: 100ms delay, 2% packet loss, rate limited to 1Mbit
sudo tc qdisc add dev enp0s3 root netem delay 100ms loss 2% rate 1mbit

# Verify that the rules were applied
echo "[INFO] Current traffic control rules:"
sudo tc qdisc show dev enp0s3
