# Example of using Python to interact with the Space and Time API 

> **[SxT Beta]**
> As of this writing the SxT API is accessible in [beta](https://www.spaceandtime.io/access-beta). In order to interact with our API, you will need an API URL which can be obtained though the link above. Also, please be aware new accounts will only get a limited number of API queries before a subscription is required. 

> [**SxT PY Examples Notebook**]
> You can find a limited example of the code in this repository in this [Colab 
Notebook](https://github.com/SxT-Community/python-api-examples/blob/main/sxt_python_api_examples.ipynb). 

## Setup & Config
1. Setup Python

These scripts were created using Python version 3.11.2 but any version of Python < 3.6 should work. If you're using Pyenv, you can create a virtualenv named: `api-test-3.11.2` and it will automatically invoke the correct python virtual env.  

2. Install Dependencies: 

`pip install -r requirements.txt`

## Generate Keys, Register User ID, & Authenticate with Space & Time 

### 1. Generate Keys 
Platform authentication (i.e. proving your identity) is based on public key cryptography, meaning you need a pair of public/private keys. 

While Space and Time supports multiple different key algorithms, we're going to keep it simple and focus on one:

- ed25519

> **Note** 
> Please see the [key algorithms section](https://docs.spaceandtime.io/docs/register-and-authenticate#key-algorithms) for more details. 

To create an Ed25519 key pair using simply execute the script:

`python generate-Ed25519-keys.py`

Output:

```shell                                                                  
Private Key (Base64): ......mufxZz6tyYj5stuwLcEd0=
Public Key (Base64): .......iR/AeJpt2F54JsNdjaJujg=
```

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
3. If not, it will register the user_id, authenticate, and return your `access_token`

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

### 3. Run a Query

[docs.spaceandtime.io/reference/execute-queries-dql](https://docs.spaceandtime.io/reference/execute-queries-dql)

Running a query against the public data in SxT is easy. For this example, we'll use the [query.py](./query.py) script. 

To access public SxT data, you only need to supply your `access_token`.  Optionally, you can also include a biscuit as a second argument if you want to query a table that requires biscuit authorization. 

In this case, we've set an environment variable for our `access_token` like:

`export AT="eyJ0eXBlIjoiYWNjZXNz..."`

So that we can simply run: 

```bash 
python query.py $AT
```

### 4. Create a table 

[https://docs.spaceandtime.io/reference/configure-resources-ddl](https://docs.spaceandtime.io/reference/configure-resources-ddl)

This is a primitive example of creating a table. Please note, this assumes that you've already created a SCHEMA to put your table in. It's also worth noting, that two new variables have been added to `.env` for this request: `BISCUIT` and `BISCUIT_PUBLIC_KEY`. 

```bash
python create.py $AT
```
