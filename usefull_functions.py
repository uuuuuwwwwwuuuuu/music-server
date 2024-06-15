import hashlib
import string
from random import choice


def encrypt_string(stringg: str):
    string_bytes = stringg.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(string_bytes)

    return hash_object.hexdigest()


def generate_id(length):
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_token(username, password):
    hashed_username = encrypt_string(username)
    hashed_password = encrypt_string(password)

    token = f'{hashed_username[:9]}{hashed_password[:9]}{generate_id(20)}'
    return token
