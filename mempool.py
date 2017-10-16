from transaction import Transaction

class MemoryPool(object):
    def __init__(self):
        # 
        """
        Transactions are stored in a Memory pool and are added to the newly mined block. 
        Each transaction is broadcasted to nodes when user wish to issue a transaction on the network. 
        Blockchain is simply a distributed ledger of these transactions.
        """
        self.pool = [] 
    
    def add_transaction(self, tx):
        if not isinstance(tx, Transaction):
            tx = Transaction(tx)

        if tx.validate_transaction():
            self.pool.append(tx)
        else:
            # log error
            print "transaction's signature is not valid"

    def remove_transactions(self, block):
        s = set(block.transactions)
        pool = [x for tx in self.pool if tx not in s]
        self.pool = pool


    def empty_pool(self):
        self.pool = []

