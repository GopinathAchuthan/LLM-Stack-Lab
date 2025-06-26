from fastapi import FastAPI
from fastapi import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to My API"}

@app.get("/posts")
async def get_posts():
    return {'data': 'This is your posts'}

@app.post("/create_post")
async def create_post(payload: dict = Body(...)):
    return {"data": payload}
    # return {"message": "successfully created post"}