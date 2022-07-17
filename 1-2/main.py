from fastapi import FastAPI

app = FastAPI()

@app.get("/transaction_pool")
def get_transaction():
    # トランザクションプールをブラウザに表示させる処理; Process to display the transaction pool in the browser
    pass
    
@app.get("/chain")
def get_chain():
    # チェーンをブラウザに表示させる処理; Process to display the chain in the browser
    pass

@app.post("/transaction_pool")
def post_transaction_pool():
    # トランザクションプールにトランザクションを追加する処理; Process of adding a transaction to the transaction pool
    pass

@app.get("/create_block")
def create_block():
    # ブロック生成処理; Block generation process
    pass