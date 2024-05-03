from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Schemas for Post Table in model -->
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool
    owner_id: int
    
    class config:
        orm_mode = True

# -->

# Schemas for users -->

class Usercreate(BaseModel):
    email:EmailStr
    password:str

class Responseuser(BaseModel):
    id:int
    email:EmailStr

    class config:
        orm_mode=True
    
class GetResponseuser(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class config:
        orm_mode=True

class User_authenticate(BaseModel):
    email:EmailStr
    password:str

# -->

# Tken schemas -->

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:Optional[str] = None

# -->