import requests
import json
from secret import *

oauth = requests_oauthlib.OAuth2Session(sandbox_payload["client_id"], redirect_uri=sandbox_payload["redirect_uri"], scope="offline_access")

authorization_url, state = oauth.authorization_url(sandbox_login_url)

print(f"Please go to {authorization_url} and authorize access.")
authorization_response = input("Enter the full callback URL: ")
sandbox_payload["code"] = authorization_response.split("?")[1].split("&")[0].split("=")[1]


response = requests.post(sandbox_token_url,data=sandbox_payload, headers=sandbox_token_headers)
data = response.json()
access_token = data["access_token"]
refresh_token = data["refresh_token"]

