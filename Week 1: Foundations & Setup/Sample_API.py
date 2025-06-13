from fastapi import FastAPI
from pydantic import BaseModel

# Step 1: Create the FastAPI app
app = FastAPI()

# Step 2: Define a data model for the request body
class Item(BaseModel):
    name: str
    description: str = None
    price: float

# Step 3: Define a GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}

# Step 4: Define a POST endpoint
@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
