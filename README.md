# ISeeYou Network Tracing and ASN Mapping

## Overview

This repository contains three Bash scripts, FullIseeYou.sh and IseeYou.sh, which utilize strace to trace system calls and extract IP addresses from network activities. These scripts map the extracted IPs to Autonomous System Numbers (ASNs), and in the case of FullIseeYou.sh, further map ASNs to their associated organizations. Additionally, a Python script, ISeeWhereYouAreToo.py, is included to perform ASN lookup and geolocation (country and state/region) for a given IP address.

## Prerequisites





- `strace`: Used to trace system calls and network activities (required for FullIseeYou.sh and IseeYou.sh).



- `Python 3:` Required for running the accompanying ASN lookup, mapping, and geolocation scripts.



Python Libraries (for ISeeWhereYouAreToo.py):





- `ipwhois`: For ASN lookup.



- `geoip2`: For geolocation.



- Install with: `pip install ipwhois geoip2`



GeoLite2 City Database (for ISeeWhereYouAreToo.py):





- Download the `GeoLite2-City.mmdb` file from MaxMind (requires a free account).



- Place `GeoLite2-City.mmdb` in the same directory as ISeeWhereYouAreToo.py.



`cymru-asnmap.py`: A Python script that queries ASN data for extracted IPs (required for FullIseeYou.sh and IseeYou.sh).



`asn_mapper.py`: A Python script that maps ASNs to organization names using a JSONL file (required for FullIseeYou.sh).

> Ensure all dependencies are installed, and the required scripts (cymru-asnmap.py, asn_mapper.py, and ISeeWhereYouAreToo.py) and database file are in the same directory as the Bash scripts.

## Scripts

### 1. FullIseeYou.sh

This script:





- Runs strace to capture system calls for a given command, focusing on network-related calls.



- Extracts IP addresses from the network-related system calls.



- Maps the extracted IP addresses to ASNs using cymru-asnmap.py.



- Maps the ASNs to organization names using asn_mapper.py.

Usage:
```
./FullIseeYou.sh <start_command>
```
Example:
```
./FullIseeYou.sh 'ngrok http 8080'
```
### 2. IseeYou.sh

This script:





- Runs strace to capture system calls for a given command, focusing on network-related calls.



- Extracts IP addresses from the network-related system calls.



- Maps the extracted IP addresses to ASNs using cymru-asnmap.py.

Usage:
```
./IseeYou.sh <start_command>
```
Example:
```
./IseeYou.sh 'ngrok http 8080'
```
### 3. ISeeWhereYouAreToo.py

This script:





- Takes a single IP address as input via the command line.



- Retrieves the ASN and ASN description using the ipwhois library.



- Determines the country and state/region (if available) using the geoip2 library with the GeoLite2 City database.



- Outputs the IP address, ASN, ASN description, country, and state/region.

Usage:
```
python ISeeWhereYouAreToo.py <IP_ADDRESS>
```
Example:
```
python ISeeWhereYouAreToo.py 8.8.8.8
```
Example Output:
```
IP Address: 8.8.8.8
ASN: 15169
ASN Description: GOOGLE, US
Country: United States
State/Region: California
```
Notes:

- Requires the GeoLite2-City.mmdb file in the same directory for geolocation. Without it, country and state/region will return 'N/A'.

- State/region data may not always be available, depending on the IP and database accuracy.

- Uses RDAP for ASN lookup, which is reliable but may occasionally fail due to network issues or rate limits.

## Output

### For FullIseeYou.sh and IseeYou.sh:

- `network_trace.log`: Logs network-related system calls.
- `full_trace.log`: Logs all system calls made by the command.
- `dns_trace.log`: Logs DNS and execve related system calls.
- `ip_addresses.txt`: List of unique IP addresses found during the strace session.
- `output-asnmap.csv`: A CSV file containing the ASN mapping for the extracted IP addresses.
- `asn-org-mapped.csv` (only in FullIseeYou.sh): A CSV file mapping ASNs to organization names.

### For ISeeWhereYouAreToo.py:

Console output with the IP address, ASN, ASN description, country, and state/region.

## How It Works

### FullIseeYou.sh and IseeYou.sh:





- The script runs strace on the provided command to capture system calls for 10 seconds (adjustable).



- IP addresses are extracted from the network-related system calls and saved to ip_addresses.txt.



- The script runs cymru-asnmap.py to map the IPs to ASNs and outputs them to output-asnmap.csv.



- FullIseeYou.sh further processes the ASNs using asn_mapper.py to map ASNs to their respective organizations.

### ISeeWhereYouAreToo.py:





- Validates the provided IP address.



- Queries RDAP using ipwhois to retrieve ASN and ASN description.



- Uses the GeoLite2 City database via geoip2 to retrieve country and state/region (if available).



- Prints the results to the console.

## Notes





- Ensure all Python scripts (cymru-asnmap.py, asn_mapper.py, and ISeeWhereYouAreToo.py) and the GeoLite2-City.mmdb file are in the same directory as the Bash scripts.



- Modify the sleep duration in FullIseeYou.sh or IseeYou.sh if needed, depending on how long you want the traced process to run.



- The Bash scripts currently kill the traced process with SIGKILL. You may modify them to use SIGINT for more graceful termination.



- For ISeeWhereYouAreToo.py, ensure a valid IPv4 address is provided. IPv6 support can be added if needed.



- The GeoLite2 City database requires periodic updates to maintain accuracy.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
