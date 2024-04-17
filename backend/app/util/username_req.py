import re

def validate_username(username):
    pattern = r'^[a-zA-Z0-9_-]{3,20}$'
    if re.match(pattern, username):
        return True
    else:
        return False
