class BlockChain(object):

    def __init__(self):
        self.transaction_pool = {"transactions": []}
        self.chain = {"blocks": []}

    def add_transaction_pool(self, transaction):
        transaction_dict = transaction.dict()
        self.transaction_pool["transactions"].append(transaction_dict)