import datetime
import json
import requests
import api_list
from ecdsa import VerifyingKey
from ecdsa import SECP256k1
import binascii
import hashlib

REWORD_AMOUNT = 999
OTHER_API_LIST = api_list.PRD_API_LIST
PROOF_OF_WORK_DIFFICULTY = 4

class BlockChain(object):
    def __init__(self):
        self.transaction_pool = {"transactions": []}
        self.chain = {"blocks": []}
        self.first_block = {
            "time": "0000-00-00T00:00:00.000000",
            "transactions": [],
            "hash": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "nonce": 0
        }
        self.chain["blocks"].append(self.first_block)

    def add_transaction_pool(self, transaction):
        transaction_dict = transaction.dict()
        self.transaction_pool["transactions"].append(transaction_dict)

    def create_new_block(self, creator):
        reword_transaction_dict = {
            "time": datetime.datetime.now().isoformat(),
            "sender": "Blockchain",
            "receiver": creator,
            "amount": REWORD_AMOUNT,
            "description": "reword",
            "signature": "not need"
        }

        transactions = self.transaction_pool["transactions"].copy()
        transactions.append(reword_transaction_dict)

        last_block_dict = self.chain["blocks"][-1]
        hash = self.hash(last_block_dict)

        block_without_time = {
            "transactions": transactions,
            "hash": hash,
            "nonce": 0
            }
        
        while not self.hash(block_without_time)[:PROOF_OF_WORK_DIFFICULTY] == '0'*PROOF_OF_WORK_DIFFICULTY:
            block_without_time["nonce"] += 1

        block = {
            "time": datetime.datetime.now().isoformat(),
            "transactions": block_without_time["transactions"],
            "hash": block_without_time["hash"],
            "nonce": block_without_time["nonce"]
        }

        self.chain["blocks"].append(block)
        
        # self.transaction_pool["transactions"] = []
        for transaction in block["transactions"]:
            if transaction in self.transaction_pool["transactions"]:
                self.transaction_pool["transactions"].remove(transaction)

    def broadcast_transaction(self, transaction):
        transaction_dict = transaction.dict()
        for url in OTHER_API_LIST:
            res = requests.post(url+"/receive_transaction", json.dumps(transaction_dict))
            print(res.json())

    def broadcast_chain(self, chain):
        for url in OTHER_API_LIST:
            res = requests.post(url+"/receive_chain", json.dumps(chain))
            print(res.json())

    def replace_chain(self, chain):       
        chain_dict = chain.dict()
        self.chain = chain_dict
        # self.transaction_pool["transactions"] = []
        latest_block_transactions = chain_dict["blocks"][-1]["transactions"]
        for transaction in latest_block_transactions:
            if transaction in self.transaction_pool["transactions"]:
                self.transaction_pool["transactions"].remove(transaction)

    def verify_transaction(self, transaction):
        public_key = VerifyingKey.from_string(binascii.unhexlify(transaction.sender), curve=SECP256k1)
        signature = binascii.unhexlify(transaction.signature)
        transaction_unsigned = {
            "time": transaction.time,
            "sender": transaction.sender,
            "receiver": transaction.receiver,
            "amount": transaction.amount,
            "description": transaction.description
        }
        transaction_unsigned_json = json.dumps(transaction_unsigned)
        transaction_unsigned_bytes = bytes(transaction_unsigned_json, encoding = "utf-8")
        return public_key.verify(signature, transaction_unsigned_bytes)

    def hash(self, block_dict):
        block_json = json.dumps(block_dict)
        block_byte = bytes(block_json, encoding = "utf-8")
        hash = hashlib.sha256(block_byte).hexdigest()
        return hash

    def verify_chain(self, chain):
        chain_dict = chain.dict()

        if len(chain_dict["blocks"]) <= len(self.chain["blocks"]):
            return False

        for i in range(len(chain_dict["blocks"])):
            block = chain_dict["blocks"][i]
            previous_block = chain_dict["blocks"][i-1]
            if i == 0:
                if block != self.first_block:
                    return False
            else:
                if block["hash"] != self.hash(previous_block):
                    return False
                block_without_time = {
                    "transactions": block["transactions"],
                    "hash": block["hash"],
                    "nonce": block["nonce"]
                }
                if self.hash(block_without_time)[:PROOF_OF_WORK_DIFFICULTY] != '0'*PROOF_OF_WORK_DIFFICULTY:
                    return False

        reword_transaction = chain_dict["blocks"][-1]["transactions"][-1]
        if reword_transaction["sender"] != "Blockchain":
            return False
        if reword_transaction["amount"] != REWORD_AMOUNT:
            return False

        return True