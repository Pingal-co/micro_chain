from utils import bin_dbl_sha256
import time



class TxInput(object):
    def __init__(self):
        """
        a list of list of the form [[previous_tx_hash, output_index]]
        outpoint:  32-byte TXID and a 4-byte output index number 
        """
        self.inputs = []

    def add(self, txs):
        for tx in txs:
            self.inputs.append([tx["previous_tx_hash"], tx["output_index"])

    def serialize(self):
        return "".join([str(inp[0]) + str(inp[1]) for inp in self.inputs]) 

class TxOutput(object):
    def __init__(self, outs=[]):
        """
        a list of list of the form [[recipient, value]]
        """
        self.outputs = outs

    def add(self, recipient, amount):
        for tx in txs:
            self.outputs.append([tx["recipient"], tx["amount"])

    def serialize(self):
        return "".join([str(out[0]) + str(out[1]) for out in self.outputs]) 

class Transaction(object):
    def __init__(self, wallet, txs):
        # 
        """
        Transaction is a datatype that contains header (Type: TxInputs, TxOutputs) and signature (Type: ByteString)
        It denotes a modification to the ledger state. 
       
        Transaction Header: a datatype that defines the stateful modification 
        senderKey: <str> address of the sender
        receiver: <str> Address of the recipient
        amount: <int> Amount
       
        Transactions are stored in a Memory pool and are added to the newly mined block. 
        Each transaction is broadcasted to nodes when user wish to issue a transaction on the network. 
        Blockchain is simply a distributed ledger of these transactions.
        """


        # a list of list of the form [[previous_tx_hash, output_index]]
        self.inputs = TxInput().add(txs)
         # a list of list of the form [[recipient, value]]
        self.outputs = TxOutput().add(txs)       
        self.public_key = wallet.get_public_key()

        signing_string = self.inputs.serialize() + self.outputs.serialize() + self.public_key
        
        self.signature = wallet.sign(signing_string)
        self.hash = self.compute_hash(signing_string + self.signature)

    def compute_hash(self, s):
        # SHA256(SHA256())
        return bin_dbl_sha256(s)

    
    def verify_transaction(self):
        pass


    def validate_transaction(self):
        """
        Holds the logic for verifying a transaction.
        Based on: https://en.bitcoin.it/wiki/Protocol_rules
        """
        if not self.header.senderKey:
            return False
        if not self.header.recipient:
            return False
        if not self.header.amount:
            return False
        if not self.sign: 
            return False
        # validate signature of the sender

        return True

    def serialize(self):
        """
        Packs a dictionary with transaction data in accordance with Bitcoin's transaction format:
        https://bitcoin.org/en/developer-reference#raw-transaction-format
        """
        pass

