#!/bin/bash

# Check for minimum arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <start_command>"
    echo "Example: $0 'ngrok http 8080'"
    exit 1
fi

# Assign start command
START_COMMAND="$1"

# Function to run strace with various options
run_strace() {
    local log_file="$1"
    local strace_options="$2"

    echo "Running strace with options: $strace_options..."
    strace -f $strace_options -o "$log_file" bash -c "$START_COMMAND" &
    TOOL_PID=$!

    # Let the tool run for a while (adjust as needed)
    sleep 10  # Change this as necessary for your use case

    # Gracefully terminate the tool with SIGINT (Ctrl+C equivalent)
    echo "Stopping the tool with PID: $TOOL_PID using SIGINT..."
    kill -SIGKILL $TOOL_PID
    
    # Wait for the process to terminate
    wait $TOOL_PID 2>/dev/null

    sleep 5
}

# Run different strace commands
run_strace "network_trace.log" "-e trace=network"
run_strace "full_trace.log" ""
run_strace "dns_trace.log" "-e trace=network,execve"

# Extract IP addresses from the network trace
echo "Extracting IP addresses from network_trace.log..."
IP_ADDRESSES=$(grep -oP '(\d{1,3}\.){3}\d{1,3}' "network_trace.log" | sort -u)

# Save the IP addresses to a temporary file
IP_FILE="ip_addresses.txt"
echo "$IP_ADDRESSES" > "$IP_FILE"

# Check if any IP addresses were found
if [[ -s "$IP_FILE" ]]; then
    echo "Found IP addresses, querying ASNs..."
    
    # Run the ASN query Python script with the extracted IPs
    python3 cymru-asnmap.py -f "$IP_FILE" -o output-asnmap.csv

    echo "Output saved to: output-asnmap.csv"
else
    echo "No IP addresses found."
fi

