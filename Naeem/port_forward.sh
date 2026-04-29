#!/bin/bash

# List of ports to handle
PORTS=(7865)

# Remote SSH host details
SSH_USER="ubuntu"
SSH_HOST="linux.ferdowsi.cloud"
SSH_PORT=2602

echo "Checking and killing processes using target ports..."
for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti tcp:$PORT)
    if [ -n "$PID" ]; then
        echo "Killing process $PID using port $PORT..."
        kill -9 "$PID" 2>/dev/null
    else
        echo "No active process found on port $PORT."
    fi
done
for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti tcp:$PORT)
    if [ -n "$PID" ]; then
        echo "Killing process $PID using port $PORT..."
        kill -9 "$PID" 2>/dev/null
    else
        echo "No active process found on port $PORT."
    fi
done
for PORT in "${PORTS[@]}"; do
    PID=$(lsof -ti tcp:$PORT)
    if [ -n "$PID" ]; then
        echo "Killing process $PID using port $PORT..."
        kill -9 "$PID" 2>/dev/null
    else
        echo "No active process found on port $PORT."
    fi
done

echo "All relevant processes cleared."
echo "Starting SSH port forwarding..."

# Tunnel 1
ssh -p $SSH_PORT -fN -L 7865:localhost:7860 $SSH_USER@$SSH_HOST

echo "All port forwardings established successfully."