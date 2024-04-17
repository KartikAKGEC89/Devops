from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from . import models
from .database import SessionLocal, engine

metadata = MetaData()
metadata.create_all(engine)

app = FastAPI()
class Post(BaseModel):
    id:int
    tittle: str
    content: str
    published: bool = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# connection part <----

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FastApi', user='postgres',
                                password='Deepak90@', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


# ------>

my_post = [{"tittle":"the hello", "id":1},{"tittle":"the hello India", "id":2},{"tittle":"the hello UK", "id":3},]


def find_post(id):
    for p in my_post:
        if p['id'] == id:
            return p
        

def delete_post(id):
    for i ,p  in enumerate(my_post):
        if p["id"] == id:
            return i
    
# Decorator to turn a plain function into an API endpoint


@app.get('/')

# Plain function with async keyword

async def root():
    return {"Message": "hello API"}

# Read from DataBase --->

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}



@app.get('/post')
async def root():
    cursor.execute("""SELECT * FROM posts;""")
    postdata = cursor.fetchall()
    print(postdata)
    return {"Data": postdata} 


# ----->

# Create new in Database --->


@app.post('/createposts')

# payLoad: dict = Body(...) :- This is helpful for managing data

async def createposts(post: Post):

    # This is helpful for print data

    # new_post_dict = new_post.dict() 
    # new_post_dict['id'] = randrange(0,1000000)

    # my_post.append(new_post_dict)

    # --> Stage changes 

    cursor.execute(""" INSERT INTO posts(tittle, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                   (post.tittle, post.content, post.published))
    new_post = cursor.fetchone()

    # -->

    # -->   Final change

    conn.commit()

    # -->

    return{"data": new_post} 


# ---->


@app.get('/post/latest')  
async def latest_post():
    post = my_post[len(my_post) -1]
    return {"details":post} 


# Fetch data by ID -->

@app.get('/post/{id}')
async def new_post(id: int, response: Response):
    # post = find_post(id)
    # if not post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
    #                         detail=f"{id} not found")
    #     # response.status_code = 404
    #     # return {"message": f"{id} not found"}

    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"{id} not found")
    print(post)
    return{"Data": f"Here post {id} find successful {post}"}

# -->


# Delete post by ID -->

@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id:int):

    # index=delete_post(id)

    # my_post.pop(index)

    cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id)))
    deletepost=cursor.fetchone()
    conn.commit()
    print(deletepost)

    # return {"meassage":"Hello Delete"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -->

# Update Post -->

@app.put("/post/{id}")
async def update_post(id:int, post:Post):
    # index=delete_post(id)
    # if index ==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post Not found {id}")
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_post[index] = post_dict
    # print(post)

    cursor.execute(""" UPDATE posts SET tittle = %s, content = %s, published = %s RETURNING *""", 
                   (post.tittle, post.content, post.published))
    updatepost = cursor.fetchone()
    conn.commit()
    
    return{"message": updatepost}

# -->