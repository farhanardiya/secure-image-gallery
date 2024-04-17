import bcrypt

def hash_password(password: str):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt).decode('utf-8')

    return hash

def check_password(password: str, hash: str):
    bytes = password.encode('utf-8')
    result = bcrypt.checkpw(bytes, hash.encode('utf-8'))

    return result
