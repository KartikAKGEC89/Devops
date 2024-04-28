from fastapi import status, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/createuser', status_code=status.HTTP_201_CREATED, response_model=schemas.Responseuser)
def create_user(user: schemas.Usercreate, db: Session = Depends(get_db)):
    
    # Hashed Password -->
    hash = utils.hasedpassword(user.password)
    user.password = hash
    # -->
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/user/{id}', response_model = schemas.GetResponseuser)
def getusers(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return {"error":"id not exist"}
    
    return user