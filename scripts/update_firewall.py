import os
import requests
import google.auth
from google.cloud import compute_v1
from google.auth.exceptions import DefaultCredentialsError
import ipaddress

GITHUB_META_API_URL = "https://api.github.com/meta"
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
FIREWALL_RULE_NAME = os.getenv('FIREWALL_RULE_NAME')
KEYS_TO_EXTRACT = ["actions", "hooks"]

def is_ipv4(ip_range):
    try:
        ipaddress.IPv4Network(ip_range)
        return True
    except ipaddress.AddressValueError:
        return False

def update_firewall_rule(ip_ranges):
    try:
        credentials, project = google.auth.default()
        service = compute_v1.FirewallsClient(credentials=credentials)

        ipv4_ranges = list(filter(is_ipv4, ip_ranges))

        firewall = service.get(project=GCP_PROJECT_ID, firewall=FIREWALL_RULE_NAME)
        firewall.source_ranges = ipv4_ranges
        operation = service.patch(project=GCP_PROJECT_ID, firewall=FIREWALL_RULE_NAME, firewall_resource=firewall)
        operation.result()
        print("Firewall rule updated successfully.")
    except DefaultCredentialsError:
        print("Google Cloud credentials not found. Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    response = requests.get(GITHUB_META_API_URL)
    if response.status_code == 200:
        data = response.json()
        ip_ranges = []
        for key in KEYS_TO_EXTRACT:
            if key not in data:
                raise ValueError(f"The key '{key}' is not found in the GitHub API response.")
            ip_ranges.extend(data.get(key, []))
        if ip_ranges:
            update_firewall_rule(ip_ranges)
        else:
            print("No IP ranges found in GitHub API response.")
    else:
        print(f"Failed to fetch data from GitHub API. Status code: {response.status_code}")


if __name__ == "__main__":
    if not all([GCP_PROJECT_ID, FIREWALL_RULE_NAME]):
        print("Please set the GCP_PROJECT_ID and FIREWALL_RULE_NAME environment variables.")
    else:
        main()
