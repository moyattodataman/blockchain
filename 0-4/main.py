from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "Japan"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}