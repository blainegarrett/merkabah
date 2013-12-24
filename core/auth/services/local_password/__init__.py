"""
Merkabah Local Password Auth Service

Passwords are encrypted using PBKDF2 using SHA1 hashing algorithm
"""
import os
from Crypto.Protocol.KDF import PBKDF2

PBKDF2_ITERATIONS = 5000
KEY_LENGTH = 32


def set_password(password, login):
    """
    Given a plain text password
    Note: This does not save the login such that you can do it in a txn, etc
    """

    salt = os.urandom(32)

    key = PBKDF2(password, salt, dkLen=KEY_LENGTH, count=PBKDF2_ITERATIONS)

    login.auth_token = salt.encode('hex')
    login.auth_data = key.encode('hex')

    return login


def check_password(password, login):
    """
    Given a plain text password, hash it and compare it to the original
    """

    salt_hex = login.auth_token
    encrypted_pw_hex = login.auth_data

    key = PBKDF2(password, salt_hex.decode('hex'), dkLen=KEY_LENGTH, count=PBKDF2_ITERATIONS)

    if key.encode('hex') == encrypted_pw_hex:
        return True
    return False
