# Example of using Python to interact with the Space and Time API 

> **Note**
> As of this writing the SxT API is accessible through the [Controlled Release](https://docs.spaceandtime.io/docs/controlled-release) program. In order to interact with our API, you will need an org/join code and the API URL which can be obtained though the link above. 

## Setup & Config
1. Setup Python

These scripts were created using Python version 3.11.2 but any version of Python 3 should work. If you're using Pyenv, you can create a virtualenv named: `api-test-3.11.2` and it will automatically invoke correct python virtual env.  

2. Install Dependencies: 

`pip install -r requirements.txt`

## Generate Keys, Register User ID, & Authenticate with Space & Time 

3. Create and populate your .env file
`cp sample.env .env`

Open `.env` file and update the variable values as necessary. 

### 1. Generate Keys 
Platform authentication (i.e. proving your identity) is based on public key cryptography, meaning you need a pair of public/private keys. 

While Space and Time supports multiple different key algorithms, we're going to keep it simple and focus on two:

- ED25519
- secp256k1 (Ethereum Accounts/Wallets)

> **Note** 
> Please see the [key algorithms section](https://docs.spaceandtime.io/docs/register-and-authenticate#key-algorithms) for more details. 

To create key pairs using both algorithms simply execute the script:

`python generate-keys.py`

Output:

```shell
Ethereum based keypair:
private key: 0xYOUR_PRIVATE_KEY_HERE
public key: 0xYOUR_PUBLIC_KEY_HERE

ED25519 based keypair:
private key: YOUR_PRIVATE_KEY_HERE=
public key: YOUR_PUBLIC_KEY_HERE=
```

You only need to select one keypair and we currently recommend using ED25519. You can always add more keys to your account but for now, we'll just need one pair. 

Save your keys to a password manager and close out the terminal window. 

> **Warning**
> It's important to note that your private keys are used to authentication to Space and Time and thus should be treated accordingly. Please do not, post, commit, or share your private keys! 

### 2. Register A New User ID
To register a new SxT user id through the API you will need three things:
1. Public/Private key pair (generated in step 1) 
2. SxT API URL 
3. Join/Org Code

Next we will add those values to a .env file: 

`cp sample.env .env`

Update the your new `.env` file with the appropriate values accordingly. 

The `register-authenticate.py` script is meant to demonstrate a few basic workflows. 

1. It will check if the user_id supplied exists
2. If it does exist, it will authenticate and return your `access_token` 
2. If not, it will register the user_id, authenticate, and return your `access_token`

`python register-authenticate.py <user_id>`

For if a user doesn't exist:

```
python register-authenticate.py b0bby
INFO:root:Checking id: b0bby with URL: XXX
INFO:root:UserID doesn't exist!
INFO:root:Lets create your user ID!
INFO:root:Authenticaiton to the SxT API has been completed successfully!
Access token: eyJ0eXBlIjoiYWNjZXNzIiwia2lkIjoiZTUxNDVkYmQtZGNmYi00ZjI4...
```

And if the user does:

```
python register-authenticate.py b0b
INFO:root:Checking id: b0b with URL: XXX
INFO:root:UserID exists!
INFO:root:Time to authenticate!
INFO:root:Authenticaiton to the SxT API has been completed successfully!
Access token: eyJ0eXBlIjoiYWNjZXNzIiwia2lkIjoiZTUxNDVkYmQtZGNmYi00ZjI4L...
```

