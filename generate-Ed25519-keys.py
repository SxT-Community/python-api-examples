# -*- coding: utf-8 -*-

import os
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

# Generate a random 32-byte seed
seed = os.urandom(32)

# Create a private key from the seed
private_key = Ed25519PrivateKey.from_private_bytes(seed)

# Get the corresponding public key
public_key = private_key.public_key()

# Encode the private and public keys as bytes
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

# Encode the private key, and public key in Base64 format
private_key_base64 = base64.b64encode(private_key_bytes)
public_key_base64 = base64.b64encode(public_key_bytes)

# Print the private key, and public key in Base64 format
print("Private Key (Base64):", private_key_base64.decode())
print("Public Key (Base64):", public_key_base64.decode())