# -*- coding: utf-8 -*-

from eth_account import Account
import secrets

def generate_eth_account(): 
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    public_key = Account.from_key(private_key)
    print('\nEthereum based keypair:')
    print("Private Key :", private_key)
    print("Public Key :", public_key.address)

generate_eth_account()


