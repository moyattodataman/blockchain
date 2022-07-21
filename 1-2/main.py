from fastapi import FastAPI

app = FastAPI()

@app.get("/transaction_pool")
def get_transaction():
    pass
    
@app.get("/chain")
def get_chain():
    pass

@app.post("/transaction_pool")
def post_transaction_pool():
    pass

@app.get("/create_block")
def create_block():
    pass