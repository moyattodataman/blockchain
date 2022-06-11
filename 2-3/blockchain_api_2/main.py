from fastapi import FastAPI
import blockchain
from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    time: str
    sender: str
    receiver: str
    amount: int
    description: str
    signature: str

class Block(BaseModel):
    time: str
    transactions: List[Transaction]
    hash: str
    nonce: int

class Chain(BaseModel):
    blocks: List[Block]

blockchain = blockchain.BlockChain()
app = FastAPI()

@app.get("/transaction_pool")
def get_transaction():
    return blockchain.transaction_pool
    
@app.get("/chain")
def get_chain():
    return blockchain.chain

@app.post("/transaction_pool")
def post_transaction_pool(transaction :Transaction):
    blockchain.add_transaction_pool(transaction)
    blockchain.broadcast_transaction(transaction)
    return { "message" : "Transaction is posted."}

@app.get("/create_block/{creator}")
def create_block(creator: str):
    blockchain.create_new_block(creator)
    blockchain.broadcast_chain(blockchain.chain)
    return {"message": "New Block is Created."}

@app.post("/receive_transaction")
def receive_transaction(transaction :Transaction):
    blockchain.add_transaction_pool(transaction)
    return { "message" : "Broadcast Transaction is success."}

@app.post("/receive_chain")
def receive_chain(chain: Chain):
    blockchain.replace_chain(chain)
    return { "message" : "Broadcast Chain is success."}