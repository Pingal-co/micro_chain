import crypto
from transaction import Transaction 

class Wallet(object):
    def __init__(self):
        self.private_key, self.public_key = crypto.gen_keypair()
        self.address = crypto.pubkey_to_address(self.public_key)

    def get_public_key(self):
        return crypto.encode_pubkey(self.public_key)
    
    def get_private_key(self)
        return crypto.encode_privkey(self.private_key)
 
    def sign(self, msg):
        return crypto.sign(msg, crypto.encode_privkey(self.private_key))

    def verify(self, msg, signature):
        return crypto.verify_sign(msg, crypto.encode_pubkey(self.public_key), signature)

    def balance(self):
        pass

    def send(self, amount, recipient):
        tx = Transaction(self, amount, recipient)

    def tx_serialize(self, tx):
        
        public_key = wallet.get_public_key()
        sign = struct.pack("<B", len(self.signature))
        sign += self.signature
        sign += struct.pack("<B", len(public_key))
        sign += public_key

        return serial
    

class Address(object):
    def __init__(self):
        """
        two enitity types:
        - user
        - contracts
        """
        pass
