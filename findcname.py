#!/usr/bin/env python3
import argparse
import subprocess
import re
from urllib.parse import urlparse

def display_logo():
    logo = """
   __ _         _  ___
  / _(_)_ _  __| |/ __|_ _  __ _ _ __  ___
 |  _| | ' \/ _` | (__| ' \/ _` | '  \/ -_)
 |_| |_|_||_\__,_|\___|_||_\__,_|_|_|_\___|
				by th3any0ne
running....
 """
    print(logo)

def get_dns_records(domain):
    # Execute the dig command
    result = subprocess.run(['dig', 'CNAME', domain], capture_output=True, text=True)
    
    # Check if the command was successful
    if result.returncode == 0:
        # Split the output into lines
        lines = result.stdout.split('\n')
        cname_records = []
        status = None
        
        # Extract the status from the header section
        for line in lines:
            if line.startswith(";; ->>HEADER<<-"):
                match = re.search(r"status: (\w+),", line)
                if match:
                    status = match.group(1)
                break

        # If status is None, there was an error extracting it
        if status is None:
            status = "Error (Status not found)"
            print(f"Error: Status not found for {domain}")

        # Iterate through the lines and extract CNAME records
        for line in lines:
            if "CNAME" in line:
                cname_records.append(line.split()[-1])

        return status, cname_records
    else:
        status = "Error (dig command failed)"
        cname_records = []
        print(f"Error executing dig command for {domain}:")
        print(result.stderr)
        return status, cname_records

def main():
    display_logo()
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Retrieve CNAME records for a list of domain names.")
    parser.add_argument("-l", "--list", help="Path to a file containing domain names, one per line.", required=True)
    args = parser.parse_args()

    # Read domain names from the file
    with open(args.list, "r") as file:
        domains = [urlparse(line.strip()).hostname for line in file.readlines() if line.strip()]

    # Retrieve and print DNS records for each domain
    for domain in domains:
        status, records = get_dns_records(domain)
        print(f"Status for {domain}: {status}")
        if status == "NOERROR":
            print(f"CNAME records for {domain}:")
            for record in records:
                print(record)
        print()

if __name__ == "__main__":
    main()

