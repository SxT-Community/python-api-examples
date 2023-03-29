# -*- coding: utf-8 -*-

from eth_account import Account
import secrets
import nacl.utils
from nacl.public import PrivateKey
import base64
import json

def generate_eth_account(): 
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    public_key = Account.from_key(private_key)
    print('\nEthereum based keypair:')
    print_keys(private_key, public_key.address)

def generate_ED25529_keys():
    # Generate a private key public key pair 
    private_key = PrivateKey.generate()
    public_key = private_key.public_key
    # base64 encode the keys 
    b64_private_key = private_key.encode(encoder=nacl.encoding.Base64Encoder)
    b64_public_key = public_key.encode(encoder=nacl.encoding.Base64Encoder)
    # print the keys (bytes to base64 string)
    print('\nED25529 based keypair:')
    print_keys(b64_private_key.decode(), b64_public_key.decode())

def print_keys(sk,pk):
    print("private key:", sk)
    print("public key:", pk)

generate_eth_account()
generate_ED25529_keys()

