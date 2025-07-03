from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import post, user, auth

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to My API"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
