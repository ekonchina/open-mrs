import base64

import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost/openmrs/ws/rest/v1"
USERNAME = "admin"
PASSWORD = "Admin123"

raw = "admin:Admin123"
token = base64.b64encode(raw.encode()).decode()


url = f"{BASE_URL}/role"

response = requests.get(
    url,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers={"Accept": "application/json"}
)

print("Status:", response.status_code)
print("Response:")
print(response.json())
