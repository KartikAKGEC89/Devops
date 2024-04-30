from fastapi import status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import utils, schemas, models

router = APIRouter(
    tags={"Authentication"}
)

@router.post('/login')
def login_user(user_credentials: schemas.User_authenticate, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    print(user)
    
    if not user:
        return {"user not found"}
    
    if not utils.verify(user_credentials.password, user.password):
        return {"Invalid credentials"}
    
    return {"Login successful"}