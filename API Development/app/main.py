from typing import Optional
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi import Body
from . import models, schemas
from .database import engine, get_db
import psycopg
import time
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to My API"}

@app.get("/sqlalchemy")
async def test_db_connection(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.Posts, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post {id} not found")
    return {"Post": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.Posts, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    update_post = post_query.first()
    return update_post