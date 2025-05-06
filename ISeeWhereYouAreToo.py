import ipwhois
import geoip2.database
import socket
import sys

def get_ip_info(ip_address):
    try:
        # Validate IP address
        socket.inet_aton(ip_address)
    except socket.error:
        print("Invalid IP address")
        return

    try:
        # Get ASN information
        whois = ipwhois.IPWhois(ip_address)
        whois_result = whois.lookup_rdap()
        
        asn = whois_result.get('asn', 'N/A')
        asn_description = whois_result.get('asn_description', 'N/A')

        # Get geolocation information (requires GeoLite2-City.mmdb database)
        try:
            reader = geoip2.database.Reader('GeoLite2-City.mmdb')
            response = reader.city(ip_address)
            
            country = response.country.name if response.country.name else 'N/A'
            state = response.subdivisions.most_specific.name if response.subdivisions.most_specific.name else 'N/A'
            
            reader.close()
        except Exception as e:
            country = state = 'N/A'
            print(f"Geolocation error: {e}")

        # Print results
        print(f"IP Address: {ip_address}")
        print(f"ASN: {asn}")
        print(f"ASN Description: {asn_description}")
        print(f"Country: {country}")
        print(f"State/Region: {state}")

    except Exception as e:
        print(f"Error retrieving information: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <IP_ADDRESS>")
        sys.exit(1)
    
    ip = sys.argv[1]
    get_ip_info(ip)
