class Consensus(object, proof=proof_of_work, complexity = 4):
    def __init__(self):
        self.proof = proof
        # complexity can be tuned depending upon the network size & the block generation rate
        self.complexity = complexity
        self.nzeros = "0" * self.complexity

    def proof_of_work(self, last_nonce):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof

        """
        nonce = 0
        while self.valid_proof(last_nonce, nonce) is False:
            nonce += 1

        return proof

    def valid_proof(last_nonce, nonce):
        """
        Validates the Proof
        :param last_nonce: <int> Previous Proof
        :param nonce: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == self.nzeros
