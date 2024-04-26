from passlib.hash import pbkdf2_sha256

def hasedpassword(password:str):
    return pbkdf2_sha256.hash(password)