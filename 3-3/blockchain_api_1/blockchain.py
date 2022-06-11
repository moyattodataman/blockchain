import datetime
import json
import requests
import api_list
from ecdsa import VerifyingKey
from ecdsa import SECP256k1
import binascii

REWORD_AMOUNT = 999
OTHER_API_LIST = api_list.DEV_API_LIST

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