from fastapi import FastAPI
import blockchain

blockchain = blockchain.BlockChain()
app = FastAPI()

@app.get("/transaction_pool")
def get_transaction():
    return blockchain.transaction_pool
    
@app.get("/chain")
def get_chain():
    return blockchain.chain

@app.post("/transaction_pool")
def post_transaction_pool():
    # トランザクションプールにトランザクションを追加する処理; Process of adding a transaction to the transaction pool
    pass

@app.get("/create_block")
def create_block():
    # ブロック生成処理; Block generation process
    pass