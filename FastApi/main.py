from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from fastapi.responses import Response


app = FastAPI()

class POST(BaseModel):
    tittle: str
    content: str
    published: bool = True
    rating: int = None



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


@app.get('/post')
async def root():
    return {"Data": my_post} 


@app.post('/createposts')

# payLoad: dict = Body(...) :- This is helpful for managing data

async def createposts(new_post: POST):

    # This is helpful for print data

    new_post_dict = new_post.dict() 
    new_post_dict['id'] = randrange(0,1000000)

    my_post.append(new_post_dict)
    return{"data": new_post} 

@app.get('/post/latest')
async def latest_post():
    post = my_post[len(my_post) -1]
    return {"details":post} 

@app.get('/post/{id}')
async def new_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"{id} not found")
        # response.status_code = 404
        # return {"message": f"{id} not found"}
    print(post)
    return{"Data": f"Here post {id} find successful {post}"}




@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id:int):

    index=delete_post(id)

    my_post.pop(index)

    # return {"meassage":"Hello Delete"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)