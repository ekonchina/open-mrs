import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost/openmrs/ws/rest/v1"
USERNAME = "admin"
PASSWORD = "Admin123"

url = f"{BASE_URL}/location"

response = requests.get(
    url,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers={"Accept": "application/json"}
)

print("Status:", response.status_code)
print("Response:")
print(response.json())
