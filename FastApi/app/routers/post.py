from fastapi import status, Depends, APIRouter, HTTPException, Response
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Post Routes"]
)


# Get data -->
@router.get("/")
def get_posts(db: Session = Depends(get_db), limits: int=10, skip:int=0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # Search from title = .filter(models.Post.title.contains(search))
    # Limit = .limit(limits)
    # Offset = .offset(skip).all()

    # similary passed in function also :-
    
    # limit = limits: int=10,
    # skip = skip:int=0,
    # search = search: Optional[str] = ""

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limits).offset(skip).all()
    return posts

# -->

# Create post -->

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

# Another method to create this same thing is use {**post.dict()} this is used to unpack the post dictionary
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    print(current_user.email)
    # way of adding one value from other table -->
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # -->
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
# -->


# Get post by id -->

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# -->


# Delete post -->
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    post = delete_post.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORRBIDEN, detail="User are not owner of the post")

    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# -->


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updatedpost = db.query(models.Post).filter(models.Post.id == id).update(post.dict())
    # if post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"post with id: {id} does not exist")
    post = updatedpost.first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORRBIDEN, detail="User are not owner of the post")
    
    db.commit()
    return {"data": updatedpost}
