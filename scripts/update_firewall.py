import os
import requests
import google.auth
from google.cloud import compute_v1

GITHUB_META_API_URL = "https://api.github.com/meta"
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
FIREWALL_RULE_NAME = os.getenv('FIREWALL_RULE_NAME')

def update_firewall_rule(ip_ranges):
    credentials, project = google.auth.default()
    service = compute_v1.FirewallsClient(credentials=credentials)

    firewall = service.get(project=GCP_PROJECT_ID, firewall=FIREWALL_RULE_NAME)
    firewall.source_ranges = ip_ranges
    operation = service.patch(project=GCP_PROJECT_ID, firewall=FIREWALL_RULE_NAME, firewall_resource=firewall)
    operation.result()

def main():
    response = requests.get(GITHUB_META_API_URL)
    ip_ranges = response.json()["actions"]
    update_firewall_rule(ip_ranges)

if __name__ == "__main__":
    main()
