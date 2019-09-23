import os
import requests
import json

if "AUTH_TOKEN" in os.environ:
    auth_token = os.environ["AUTH_TOKEN"]
else:
    raise "No auth token supplied -- use $AUTH_TOKEN environment variable"

headers = {
    "Authorization": f"{auth_token}",
    "Content-Type": "application/json"
}

params = {
    "page[size]": 10000
}

r = requests.get("https://api.oregonstate.edu/v1/locations",
                 params, headers=headers)

r.raise_for_status()

data = json.loads(r.text)

locations = data["data"]

corvallis_locations = [location for location in data['data']
                       if location['attributes']['campus'] == 'Corvallis']

print(f"{100 * len(corvallis_locations) / len(locations)}% of locations are in Corvallis")
