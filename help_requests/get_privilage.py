import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost/openmrs/ws/rest/v1"
USERNAME = "admin"
PASSWORD = "Admin123"

ROLE_UUID = "8d94f852-c2cc-11de-8d13-0010c6dffd0f"  # например: System Developer

url = f"{BASE_URL}/role/{ROLE_UUID}?v=full"

response = requests.get(
    url,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers={"Accept": "application/json"}
)

print("Status:", response.status_code)

data = response.json()

print("Role:", data.get("display"))
print("Privileges:")

for privilege in data.get("privileges", []):
    print("-", privilege.get("display"))
