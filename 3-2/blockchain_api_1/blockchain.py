import datetime
import json
import requests
import api_list

REWORD_AMOUNT = 999
OTHER_API_LIST = api_list.PRD_API_LIST

class BlockChain(object):
    def __init__(self):
        self.transaction_pool = {"transactions": []}
        self.chain = {"blocks": []}

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

        block = {
            "time": datetime.datetime.now().isoformat(),
            "transactions": transactions,
            "hash": "hash_sample",
            "nonce": 0
        }

        self.chain["blocks"].append(block)
        self.transaction_pool["transactions"] = []

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
        self.transaction_pool["transactions"] = []