from pydantic import BaseModel, EmailStr


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
    
    class config:
        orm_mode = True

class Usercreate(BaseModel):
    email:EmailStr
    password:str

class Responseuser(BaseModel):
    email:EmailStr
    id:int

    class config:
        orm_mode=True