import csv
import json

def load_asn_org_mapping(jsonl_file):
    asn_org_map = {}
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            asn = data.get("asn")
            name = data.get("name")
            if asn and name:
                asn_org_map[asn] = name
    return asn_org_map

def main(csv_file, jsonl_file, output_file):
    # Load ASN organization mapping
    asn_org_map = load_asn_org_mapping(jsonl_file)

    # Collect ASNs from the output CSV
    asn_set = set()  # Use a set for unique ASNs
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            asn = row['AS']
            if asn and asn != "NA":  # Ensure we are not taking NA values
                asn_set.add(asn)

    # Print the found ASNs
    print(f"Found ASNs: {', '.join(asn_set)}")

    # Prepare to write the mapped ASNs to the output file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['ASN', 'Organization Name'])  # Write the header

        print("Mapped ASNs:")
        for asn in asn_set:
            if asn in asn_org_map:
                org_name = asn_org_map[asn]
                writer.writerow([asn, org_name])  # Write the mapped ASN and org name
                print(f"{asn} -> {org_name}")
            else:
                print(f"{asn} not found in mapping.")

if __name__ == "__main__":
    # File names (modify if necessary)
    csv_file = 'output-asnmap.csv'
    jsonl_file = 'asn-org.jsonl'
    output_file = 'mapped_asns.csv'

    # Run the main function
    main(csv_file, jsonl_file, output_file)

