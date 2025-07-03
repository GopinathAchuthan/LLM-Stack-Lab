from typing import List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Depends
from app import models, schemas
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.utils import hash_password


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to My API"}

@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.Posts, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post {id} not found")
    return post

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



@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user