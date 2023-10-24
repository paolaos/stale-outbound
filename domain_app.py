import requests
import json
import time
from google.cloud import domains_v1

project_id = "YOUR_GCP_PROJECT_ID"
gd_key = "3mM44UdBCo5fTM_CwccjBrXir4sswgPKs2Ddx"
gd_secret = "L6VkGD14FXWm16HWzVyY1F"
auth_code = "YOUR_GODADDY_AUTH_CODE"
domain_name = "example.com"



body = {
    "domainName": "YOUR_DOMAIN_NAME",
    "tld": "YOUR_TLD",
    "years": 1,
}

headers = {
    f"Authorization: sso-key {gd_key}:{gd_secret}"
}

response = requests.post("https://api.ote-godaddy.com/v1/domains", headers=headers, data=json.dumps(body))


response = requests.post(f"https://api.godaddy.com/v1/domains/{domain_name}/purchase", headers=headers)

# Create a Cloud Domains client
client = domains_v1.DomainsClient()

# Add the domain to Cloud Domains
request = domains_v1.RegisterDomainRequest(
    domain_name=domain_name
)
response = client.register_domain(request)

# Verify the domain ownership
request = domains_v1.VerifyDomainRequest(
    domain_name=domain_name
)
response = client.verify_domain(request)

# Wait for the domain to be verified
while not response.is_verified():
    time.sleep(10)

# Set up DNS for the domain
request = domains_v1.UpdateDomainRequest(
    domain_name=domain_name,
    dns_records=[
        # MX record
        domains_v1.DnsRecord(
            name="@" + domain_name,
            type="MX",
            data="mail." + domain_name,
            priority=10
        ),

        # TXT record for Google Analytics
        domains_v1.DnsRecord(
            name="@" + domain_name,
            type="TXT",
            data="google-site-verification=XXXXXXXXXXXXXXXX"
        )
    ]
)
response = client.update_domain(request)
