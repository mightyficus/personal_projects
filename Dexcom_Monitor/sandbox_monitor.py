import requests
from secrets import *

url = "https://sandbox-api.dexcom.com"

response = requests.post(url, data=sandbox_payload, headers=sandbox_token_headers)

print(response.status_code)
#data = response.json()
#print(data)