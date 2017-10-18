from utils import bin_dbl_sha256
import time


class TxInput(object):
    def __init__(self, tx):
        """
        a data type of the form (previous_tx_hash, output_index)
        outpoint:  32-byte TXID and a 4-byte output index number 
        """
        self.previous_tx_hash = tx["previous_tx_hash"]
        self.output_index = tx["output_index"]

class TxOutput(object):
    def __init__(self, tx):
        """
        a data type of the form (recipient, value)
        """
        self.recipient = tx["recipient"], 
        self.amount = tx["amount"]

class TxInputs(object):
    def __init__(self):
        """
        a list of list of the form [[previous_tx_hash, output_index]]
        outpoint:  32-byte TXID and a 4-byte output index number 
        """
        self.data = []

    def add(self, txs):
        for tx in txs:
            self.data.append(TxInput(tx))

    def serialize(self):
        return "".join([str(d.previous_tx_hash) + str(d.output_index) for d in self.data]) 

class TxOutputs(object):
    def __init__(self):
        """
        a list of list of the form [[recipient, value]]
        """
        self.data = []

    def add(self, recipient, amount):
        for tx in txs:
            self.data.append(TxOutput(tx))

    def serialize(self):
        return "".join([str(d.recipient) + str(d.amount) for d in self.data]) 

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

                
    def serialize(self):
        """
        Packs a dictionary with transaction data in accordance with Bitcoin's transaction format:
        https://bitcoin.org/en/developer-reference#raw-transaction-format
        """
        pass

def validate_transaction(tx):
    """
    Holds the logic for verifying a transaction.
    Based on: https://en.bitcoin.it/wiki/Protocol_rules
    """
    if invalid_format(tx):
        False
        
    # validate signature of the sender
    if tx_already_exists(tx):
        False

    if ensure_inputs_not_already_spent(tx):
        False

    if ensure_inputs_ownership(tx):
        return False

    if ensure_inputs_sum_greater_than_outputs(tx):
        return False

    if ensure_public_key_ownsership(tx):
        return False

    return True

def invalid_format(tx):
    if len(tx.inputs) <= 0 :
        return True
    if len(tx.outputs) <= 0 :
        return True 
    if not is_sha256(tx.hash):
        return True 
    if not tx.signature:  
        return True

    for d in tx.inputs.data:
        valid = is_sha256(d.previous_tx_hash) and  d.output_index >= 0):
        if not valid:
            return True

    for d in tx.outputs.data:
        valid = is_ripemd160(d.recipient) and d.amount > 0
        if not valid:
            return True


def tx_already_exists(tx):
    return False

def ensure_inputs_not_already_spent(tx):
    return False

def ensure_inputs_ownership(tx):
    return False

def ensure_inputs_sum_greater_than_outputs(tx):
    return False

def ensure_public_key_ownsership(tx):
    return False
