#!/usr/bin/python
"""Copyright (c) 2016, Daniel C. Marques
All rights reserved.
...
"""

import socket
import csv
import argparse
from netaddr import IPNetwork


def to_csv(data, filename):
    """ Parses and cleans up the query response and generates a CSV file with
    the result.
    """
    with open(filename, "w", newline='') as csvfile:  # Changed "wb" to "w" for Python 3
        csvwriter = csv.writer(csvfile, delimiter=';',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(["AS", "IP", "BGP Prefix", "CC", "Registry",
                            "Allocated", "Info", "AS Name"])

        for line in data.decode().split('\n')[1:]:  # Decode the bytes response to str
            csvwriter.writerow([column.rstrip(" ").lstrip(" ")
                                for column in line.split("|")])


def query(bulk_query, timeout):
    """ Connects to the whois server and sends the bulk query. Returns the
    result of this query.
    """
    try:
        data = b""  # Initialize as bytes
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(("whois.cymru.com", 43))
        s.sendall(bulk_query.encode('utf-8'))  # Encode the query string to bytes
        reply = s.recv(4098)
        data += reply
        # Gets data until an empty line is found.
        while True:
            reply = s.recv(1024)
            if not reply:
                break
            data += reply
    except socket.timeout:
        if data != b'':
            pass
        else:
            raise
    except Exception as e:
        raise e
    finally:
        s.close()

    return data


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("target", help="Target to be queried (CIDR or filename).")
        parser.add_argument("-f", "--file", help="Loads the IPs from a file.",
                            dest="from_file", action="store_true")
        parser.add_argument("-t", "--timeout", type=int, dest="timeout",
                            default=5, help="Timeout (default is 5).")
        parser.add_argument("-o", "--output", help="Output CSV file.",
                            dest="filename")
        args = parser.parse_args()

        if args.filename:
            filename = args.filename  # Fixed here
        else:
            filename = "output-asnmap.csv"

        if args.from_file:
            with open(args.target, "r") as input_file:  # Changed to "r" for text mode
                ips = input_file.read().rstrip("\n")
        else:
            net = IPNetwork(args.target)
            ips = "\n".join([str(ip) for ip in list(net)])

        # Creates the file for bulk submission
        bulk_query = "begin\nverbose\n%s\nend\n" % ips  # Added newline at end

        response = query(bulk_query, args.timeout)

        print(response.decode())  # Decode before printing

        to_csv(response, filename)
        print("Output saved to: %s" % filename)

    except Exception as e:
        print("Unable to proceed. Error: %s" % e)

if __name__ == '__main__':
    main()
