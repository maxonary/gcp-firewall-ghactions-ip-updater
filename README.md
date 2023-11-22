# Firewall Update Tool

This repository includes scripts that automate the synchronisation of GCP firewall rules based on the IP range of GitHub Actions (https://api.github.com/meta).

## Setup

1. Make sure to have Python 3.8 or higher installed.
2. Install the dependencies from: `pip install -r requirements.txt`.
3. Configure the environment variables from the scripts.

## Usage

Run the script manually with `python ./scripts/update_firewall.py` or use the provided GitHub Actions Workflow.

- Make sure the Google Cloud Platform Service Account has the necessary permissions.
- Keep your API keys and service account information secure.