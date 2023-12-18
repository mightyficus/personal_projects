import json
from datetime import datetime, timedelta
import requests_oauthlib
import requests

# Dexcom keys

#OAuth sandbox= https://sandbox-api.dexcom.com/v2/oauth2/login?client_id=RQIV6uITTn5TOi2fbmDC7MRhZVUTedEa&redirect_uri=http://localhost:8080&response_type=code&scope=offline_access
#sandbox_code=ae2d9c3cd219230c1bbba71316b3ff5c


sandbox_login_url = "https://sandbox-api.dexcom.com/v2/oauth2/login"
sandbox_token_url= "https://sandbox-api.dexcom.com/v2/oauth2/token"

sandbox_token_headers = {"Content-Type": "application/x-www-form-urlencoded"}

def get_secrets():
    # These are variables we will use throughout the program
    global sandbox_payload
    global sandbox_auth_header

    # Get values from secret.txt
    with open("secret.txt", 'r') as ifile:
        sandbox_payload = json.load(ifile)
    
    url = "https://api.dexcom.com/v3/users/self/egvs"
    query = {
        "startDate": str(datetime.now().isoformat(sep="T", timespec="seconds")),
        "endDate": str(datetime.now().isoformat(sep="T", timespec="seconds"))
    }
    sandbox_auth_header = {"Authorization": f"Bearer {sandbox_payload['access_token']}"}

    response = requests.get(url,headers=sandbox_auth_header, params=query)

    print(type(response.status_code))

    

get_secrets()