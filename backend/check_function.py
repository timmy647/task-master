import re

def is_valid_email(email):
    if type(email) != str:
        return False
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return (re.fullmatch(regex, email))

def is_valid_password(password):
    if type(password) != str:
        return False
    if len(password) < 8 or len(password) > 50:
        return False

    if password.islower():
        return False

    if password.isupper():
        return False

    if password.isdigit():
        return False

    special_character = ["!", "@", "#", "$", "%", "^", "&", "*"]
    for a in password:
        if a in special_character:
            return True
    return False

def is_oline(user_id, online_user):
    for user in online_user:
        if user.get_user_id() == user_id:
            return user
    return None

def is_valid_name(name):
    return type(name) == str and len(name) >= 1 and len(name) <= 20

def token_check(token, online_user):
    for user in online_user:
        if user.get_token() == token:
            return user
    return None
