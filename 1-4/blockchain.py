class BlockChain(object):

    def __init__(self):
        self.transaction_pool = {"transactions": []}
        self.chain = {"blocks": []}