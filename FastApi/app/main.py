from fastapi import FastAPI

# Partof connection import -->
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# -->

from . import models
from .database import engine
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# # Connection -->

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='FastApi', user='postgres',
#                                 password='Deepak90@', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
# # -->


@app.get("/")
def root():
    return {"message": "Hello World"}

# Router -->

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# -->
