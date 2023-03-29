# -*- coding: utf-8 -*-
import requests
import sys
import json
import logging
from nacl.signing import SigningKey
import base64
from dotenv import dotenv_values

config = dotenv_values(".env")
logging.basicConfig(level=logging.INFO)
headers = {"accept": "application/json"}

# Get command line args
try:
    user_id = sys.argv[1]
except:
    logging.error('Please supply your existing or desired user_id!')
    sys.exit() 

try: 
    api_url = config['API_URL']
except:
    logging.error('Please make sure you set the SxT API_URL value in your .env file!')
    sys.exit()
try: 
    org_code = config['ORG_CODE']
    user_private_key = config['USER_PRIVATE_KEY']
    user_public_key = config['USER_PUBLIC_KEY']
except:
    logging.warning('Without ORG_CODE, and KEYS set, this script will be limited to checking if user_ids exist!')
     
def main():
    #1) Check is user_id exists, if not, register it
    if not user_id_exists():
        logging.info('Lets create your user ID!')
        authenticate()
    #2) If user_id already exists, then authenticate 
    else:
        logging.info('Time to authenticate!')
        authenticate()

# https://docs.spaceandtime.io/reference/user-identifier-check
def user_id_exists():
    url = api_url + "auth/idexists/" + user_id
    logging.info(f'Checking id: {user_id} with URL: {url}')

    resp = requests.get(url, headers=headers)
    
    if resp.status_code == 200 and resp.text == 'true':
        logging.info("UserID exists!")
        return True
    elif resp.status_code == 200 and resp.text == 'false':
        logging.info("UserID doesn't exist!")
        return False
    else: 
        logging.error("We did not connect with the SxT API successfully!")
        logging.error(resp.status_code, resp.text)
        sys.exit()

# https://docs.spaceandtime.io/reference/authentication-code
def authenticate():
    # 1) Request auth code from SxT API 
    auth_code = request_auth_code()

    # 2) Sign the auth code with our private key
    signed_auth_code = sign_message(auth_code)
    
    # 3) Request access token using signed_auth_code 
    access_token, refresh_token = request_token(auth_code, signed_auth_code)
    
    logging.info(f'Authenticaiton to the SxT API has been completed successfully!\n Access token: {access_token}\n Refresh token: {refresh_token}')
    return 

# https://docs.spaceandtime.io/reference/authentication-code
def request_auth_code():
    url = api_url + "auth/code"
    payload = {
        "userId": user_id,
        "joinCode": org_code
    }
    resp = requests.post(url, json=payload, headers=headers)
   
    jsonResponse = resp.json()
    logging.debug(f'auth/code response: {jsonResponse}')

    if resp.status_code == 200: 
        auth_code = jsonResponse["authCode"]
    else: 
        print('Non 200 response from the auth/code endpoint! Stopping.')
        sys.exit()

    return auth_code 

def sign_message(auth_code):
    # get bytes of the auth code for signing  
    bytes_message = bytes(auth_code, 'utf-8')
    # decode private key for signing 
    key = base64.b64decode(user_private_key)
    # create signing key
    signingkey = SigningKey(key)
    # finally, sign the auth code with our private key
    signed_message = signingkey.sign(bytes_message)

    logging.debug("Signature | hashed message, hex: " + signed_message.hex())
    logging.debug("Signature, hex: " + signed_message[:64].hex())

    return signed_message[:64].hex()

# https://docs.spaceandtime.io/reference/token-request
def request_token(auth_code, signed_auth_code):

    url = api_url + "auth/token"
    payload = {
        "userId": user_id,
        "authCode": auth_code,
        "signature": signed_auth_code,
        "key": user_public_key,
        "scheme": config['AUTH_SCHEME']
    }

    resp = requests.post(url, json=payload, headers=headers)
    
    if resp.status_code != 200:
        logging.error('Failed to request token from the API!')
        logging.error(resp.status_code, resp.text)
        sys.exit()
    
    jsonResp = resp.json()
    logging.debug(f'auth/token response: {jsonResp}')

    return jsonResp["accessToken"],jsonResp["refreshToken"]


if __name__ == "__main__":
    main()

   