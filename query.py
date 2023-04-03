import requests
import sys
import json
import logging
from dotenv import dotenv_values

config = dotenv_values(".env")
logging.basicConfig(level=logging.INFO)
headers = {"accept": "application/json"}

# to run
# python query.py <access_token> [<biscuit>]

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
    # https://docs.spaceandtime.io/reference/execute-queries-dql
    url = api_url + "sql/dql"
    
    # Get five transactions 
    payload = { 
        "resourceId": "ETHEREUM.TRANSACTIONS",
        "sqlText": "SELECT * FROM ETHEREUM.TRANSACTIONS LIMIT 5"
    }
    
    """ Get the latest Ethereum block 
    payload = {
        "resourceId": "ETHEREUM.TRANSACTIONS",
        "sqlText": "SELECT MAX(BLOCK_NUMBER) FROM ETHEREUM.TRANSACTIONS;"
    }
    """
    """ SxT Docs API workflow example - get dapp user wallets
    payload = {
        "resourceId": "SE_PLAYGROUND.DAPP_USER_WALLETS_1",
        "sqlText": "SELECT * FROM SE_PLAYGROUND.DAPP_USER_WALLETS_1 WHERE USER_SUBSCRIPTION = 'prime';"
    }
    """
    headers = {
        "accept": "application/json",
        "biscuit": biscuit,
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    resp = requests.post(url, json=payload, headers=headers)
    
    try: 
        json_resp = json.loads(resp.text)
        api_resposne = json.dumps(json_resp, indent=2)
    except:
        # if we don't get valid json response from the API
        api_resposne = resp.text
    
    print(f"SxT API response code: {resp.status_code}\nSxT API Response text: {api_resposne}")

if __name__ == "__main__":
    main()



