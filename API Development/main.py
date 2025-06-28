from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi import Body
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

my_posts = [{
                "title":"top place in tamilnadu",
                "content":"Chennai, Madurai, Salam",
                "publish": False,
                "rating": 3,
                "id": 1
             },
             {
                "title":"top place in TN",
                "content":"Vellore, Salam, Coimbatore",
                "publish": True,
                "rating": 5,
                "id": 2
             }]

def find_post(id):
    for p in my_posts:
        print(p)
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message": "Welcome to My API"}

@app.get("/posts")
async def get_posts():
    return {'data': 'This is your posts'}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = my_posts[-1]["id"] + 1
    my_posts.append(post_dict)    
    return {"data": my_posts[-1]}


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID - {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error msg": f"ID - {id} is not found"}
    return {"Post": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
