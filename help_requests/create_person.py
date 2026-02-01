import requests
from requests.auth import HTTPBasicAuth
import json

BASE_URL = "http://localhost/openmrs/ws/rest/v1"
USERNAME = "admin"
PASSWORD = "Admin123"

url = f"{BASE_URL}/person"

payload = {
    "names": [
        {
            "givenName": "John",
            "familyName": "Doe"
        }
    ],
    "gender": "M",
    "age": 30
}

response = requests.post(
    url,
    auth=HTTPBasicAuth(USERNAME, PASSWORD),
    headers={
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
    data=json.dumps(payload)
)

print("Status:", response.status_code)
print("Response:")
print(response.json())
