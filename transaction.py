class TransactionHeader(object):
    def __init__(self, senderKey, recipient, amount):
        """
        Transaction Header: a datatype that defines the stateful modification 
                senderKey: <str> address of the sender
                receiver: <str> Address of the recipient
                amount: <int> Amount
        """
        self.senderKey = senderKey or None
        self.recipient = recipient or None
        self.amount = amount or None

class Transaction(object):
    def __init__(self, tx={}):
        # 
        """
        Transaction is a datatype that contains header (Type: Transaction Header) and signature (Type: ByteString)
        It denotes a modification to the ledger state. 
        Transactions are stored in a Memory pool and are added to the newly mined block. 
        Each transaction is broadcasted to nodes when user wish to issue a transaction on the network. 
        Blockchain is simply a distributed ledger of these transactions.
        """
        self.header = TransactionHeader(
            senderKey = tx["senderKey"],
            recipient = tx["recipient"],
            amount = tx["amount"])
        self.signature = tx["sign"]
    
    def validate_transaction(self, tx):
        if not tx.header.senderKey:
            return False
        if not tx.header.recipient:
            return False
        if not tx.header.amount:
            return False
        if not tx.sign: 
            return False
        # validate signature of the sender

        return True

    def verify_transaction:
        # validate signature of the sender 
        pass 
