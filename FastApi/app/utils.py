from passlib.hash import bcrypt

# Hashed Password -->
def hasedpassword(password:str):
    return bcrypt.hash(password)
# -->
#  Unhashed Password -->
def verify(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)
# -->