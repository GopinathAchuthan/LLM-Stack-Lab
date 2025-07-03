from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to My API"}

app.include_router(post.router)
app.include_router(user.router)