import requests
import sys
import json
import logging
from dotenv import dotenv_values

config = dotenv_values(".env")
logging.basicConfig(level=logging.INFO)
headers = {"accept": "application/json"}

try:
    access_token = sys.argv[1]
except:
    logging.error('This script requires an SxT access_token: python query.py <your-access-token-here>')
    sys.exit() 

try: 
    biscuit = sys.argv[2]
except:
    biscuit = "" 
    logging.info('No biscuit provided. Non public data queries will require a biscuit.')
 
try: 
    api_url = config['API_URL']
except:
    logging.error('Please make sure you set the SxT API_URL value in your .env file!')
    sys.exit() 

def main():
    # https://docs.spaceandtime.io/reference/subscription-overview
    url = api_url + "subscription"

    headers = {
        "accept": "*/*",
        "authorization": f"Bearer {access_token}"
    }

    resp = requests.get(url, headers=headers)
    
    try: 
        json_resp = json.loads(resp.text)
        api_resposne = json.dumps(json_resp, indent=2)
    except:
        # if we don't get valid json response from the API
        api_resposne = resp.text
    
    print(f"SxT API response code: {resp.status_code}\nSxT API Response text: {api_resposne}")

if __name__ == "__main__":
    main()

