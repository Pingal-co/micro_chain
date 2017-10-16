class Wallet(object):
    def __init__(self):
        pass

    def public_key(self):
        pass
    
    def private_key(self)
        pass

    def address(self):
        """
        x,y = keys.public_key()
        address(x,y) = addrHash(string(x) <> string(y))
        addrHash(n) = sha256(sha256(ripemd160(sha256(n))))

        """
        pass

class Address(object):
    def __init__(self):
        """
        two enitity types:
        - user
        - contracts
        """
        pass
