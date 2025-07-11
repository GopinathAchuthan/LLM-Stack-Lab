from typing import List, Optional
from fastapi import Response, status, HTTPException
from fastapi import Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

'''
GET Requests
'''
@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db), 
                    curr_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.publish==True, models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post {id} not found")
    return post


'''
POST Requests
'''
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.Posts, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), owner_id = curr_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

'''
DELETE Requests
'''
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id ==id, models.Post.owner_id==curr_user)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} does not exist")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

'''
PUT Requests
'''
@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, post: schemas.Posts, db: Session = Depends(get_db), curr_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id ==id, models.Post.owner_id==curr_user)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id:{id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    update_post = post_query.first()
    return update_post