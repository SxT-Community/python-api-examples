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
    logging.error('This script requires an SxT access_token: python create.py <your-access-token-here>')
    sys.exit() 

try: 
    biscuit = config['BISCUIT']
except:
    logging.error('A biscuit token is required to create a table with this script. Please set BISCUIT in .env')
    sys.exit()

try: 
    biscuit_public_key = config['BISCUIT_PUBLIC_KEY']
except:
    logging.error('A biscuit public key is required to create a table with this script. Please set BISCUIT_PUB_KEY in .env')
    sys.exit()
 
try: 
    api_url = config['API_URL']
except:
    logging.error('Please make sure you set the SxT API_URL value in your .env file!')
    sys.exit() 

def main():
    # https://docs.spaceandtime.io/reference/modify-data-dml
    url = api_url + "sql/ddl"
    
    sqlText = f"CREATE TABLE SE_PLAYGROUND.DNFT_0 (player_address VARCHAR PRIMARY KEY, player_score INTEGER) WITH \
        \"public_key={biscuit_public_key},access_type=public_read\""
    
    payload = {
        "resourceId": "SE_PLAYGROUND.DNFT_0",
        "sqlText": sqlText
    }

    headers = {
        "accept": "application/json",
        "biscuit": biscuit,
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }
    logging.info(f"\nRequest Headers:{headers}\n\nRequest Payload: {payload}")
    resp = requests.post(url, json=payload, headers=headers)
    
    try: 
        json_resp = json.loads(resp.text)
        api_resposne = json.dumps(json_resp, indent=2)
    except:
        # if we don't get valid json response from the API
        api_resposne = resp.text
    
    logging.info(f"SxT API response code: {resp.status_code}\nSxT API Response text: {api_resposne}")
    

if __name__ == "__main__":
    main()
