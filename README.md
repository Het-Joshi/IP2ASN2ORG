

# ISeeYou Network Tracing and ASN Mapping

## Overview

This repository contains two Bash scripts, **FullIseeYou.sh** and **IseeYou.sh**, which utilize `strace` to trace system calls and extract IP addresses from network activities. The scripts then map these IPs to Autonomous System Numbers (ASNs) and, in the case of **FullIseeYou.sh**, further map the ASNs to their associated organizations.

## Prerequisites

- **strace**: Used to trace system calls and network activities.
- **Python 3**: Required for running the accompanying ASN lookup and mapping scripts.
- **cymru-asnmap.py**: A Python script that queries ASN data for the extracted IPs.
- **asn_mapper.py**: A Python script that maps ASNs to their corresponding organization names using a JSONL file.

Make sure all dependencies are installed, and the `cymru-asnmap.py` and `asn_mapper.py` scripts are in the same directory as the Bash scripts.

## Scripts

### 1. FullIseeYou.sh

This script:
- Runs `strace` to capture system calls for a given command, focusing on network-related calls.
- Extracts IP addresses from the network-related system calls.
- Maps the extracted IP addresses to ASNs using `cymru-asnmap.py`.
- Maps the ASNs to organization names using `asn_mapper.py`.

#### Usage:
```bash
./FullIseeYou.sh <start_command>
```

Example:
```bash
./FullIseeYou.sh 'ngrok http 8080'
```

### 2. IseeYou.sh

This script:
- Runs `strace` to capture system calls for a given command, focusing on network-related calls.
- Extracts IP addresses from the network-related system calls.
- Maps the extracted IP addresses to ASNs using `cymru-asnmap.py`.

#### Usage:
```bash
./IseeYou.sh <start_command>
```

Example:
```bash
./IseeYou.sh 'ngrok http 8080'
```

## Output

- **network_trace.log**: Logs network-related system calls.
- **full_trace.log**: Logs all system calls made by the command.
- **dns_trace.log**: Logs DNS and `execve` related system calls.
- **ip_addresses.txt**: List of unique IP addresses found during the `strace` session.
- **output-asnmap.csv**: A CSV file containing the ASN mapping for the extracted IP addresses.
- **asn-org-mapped.csv** (only in FullIseeYou.sh): A CSV file mapping ASNs to organization names.

## How It Works

1. The script runs `strace` on the provided command to capture system calls for 10 seconds (adjustable).
2. IP addresses are extracted from the network-related system calls and saved to `ip_addresses.txt`.
3. The script runs the Python script `cymru-asnmap.py` to map the IPs to ASNs and outputs them to `output-asnmap.csv`.
4. **FullIseeYou.sh** further processes the ASNs using `asn_mapper.py` to map the ASNs to their respective organizations.

## Notes

- Ensure both Python scripts (`cymru-asnmap.py` and `asn_mapper.py`) are in the same directory.
- Modify the `sleep` duration in the script if needed, depending on how long you want the traced process to run.
- The script currently kills the traced process with `SIGKILL`. You may modify it to use `SIGINT` for more graceful termination.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
