class Crypto(object):
    def __init__(object):
        pass

    def sign_transaction(self, tx):
        pass

    def verify_transaction(self, tx):
        pass

    def sign_block(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
