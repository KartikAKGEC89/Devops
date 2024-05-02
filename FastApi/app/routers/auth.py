from fastapi import status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import utils, schemas, models, oauth2

router = APIRouter(
    tags={"Authentication"}
)

@router.post('/login')
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print(user)
    
    if not user:
        return {"user not found"}
    
    if not utils.verify(user_credentials.password, user.password):
        return {"Invalid credentials"}
    

    access = oauth2.create_access_token(data={"user id":user.id})
    
    return {"access_token": access, "Token_type":"Bearer"}