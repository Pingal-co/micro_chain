
import hashlib

class BlockHeader(object):
        """
        BlockHeader = BlockHeader
        { origin       :: Key.PublicKey -- ^ Public Key of Block miner
        , previousHash :: ByteString    -- ^ Previous block hash
        , merkleRoot   :: ByteString    -- ^ Merkle root of tranactions
        , nonce        :: Int           -- ^ Nonce for Proof-of-Work
        } 
        """
    def __init__(self, miner_pubkey, previous_hash, nonce, merkle_root):
        self.miner = miner_pubkey
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = merkle_root


class Block(object):
    def __init__(self, index, previous_block, nonce, transactions, miner_pubkey, miner_signature, merkle_root):
        """
        type Index      = Int
        type Timestamp  = Integer
        type Blockchain = [Block]

        Block = Block
        { index        :: Index         -- ^ Block height
        , header       :: BlockHeader   -- ^ Block header
        , transactions :: [Transaction] -- ^ List of Transactions
        , signature    :: ByteString    -- ^ Block ECDSA signature
        }

        """
        self.index = index
        self.header = BlockHeader(miner_pubkey, self.hash(previous_block), nonce, merkle_root)
        self.transactions= transactions
        self.signature = miner_signature

    def add_genesis_block(self):
        pass

    def hash(self):
        """
            creates a SHA-256 hash of a Block
        """
        # ordered dictionary hash
        block_serialized = json.dumps(self, sort_keys=True).encode()
        return hashlib.sha256(block_serialized).hexdigest()

    def validate_block(self, prev_block):
        """
        InvalidBlock
        = InvalidBlockSignature Text
        | InvalidBlockIndex
        | InvalidBlockHash
        | InvalidBlockNumTxs
        | InvalidBlockTx T.InvalidTx
        | InvalidPrevBlockHash
        | InvalidFirstBlock
        | InvalidOriginAddress Address
        | InvalidBlockTxs [T.InvalidTx]
        """
        if self.invalid_block_signature():
            return False
        if self.invalid_block_index():
            return False
        if self.invalid_block_hash():
            return False
        if self.invalid_block_num_txs():
            return False
        if self.invalid_block_transactions():
            return False
        if self.invalid_prev_block_hash(prev_block):
            return False
        if self.invalid_first_block():
            return False
        if self.invalid_origin_address():
            return False
        if self.invalid_proof_of_work(prev_block):
            return False

        return True

    def invalid_block_signature(self, text):
        pass
    
    def invalid_block_index(self):
        pass

    def invalid_block_hash(self):
        pass

    def invalid_block_num_txs(self):
        pass

    def invalid_block_transactions(self):
        # validate all transactions
        pass

    def invalid_prev_block_hash(self, prev_block):
        return self.header.previous_hash != self.hash(prev_block)

    def invalid_first_block(self):
        pass

    def invalid_origin_address(self):
        # check the address
        pass

    def invalid_proof_of_work(self, prev_block):
        # check the nonce
        guess = f'{prev_block.header.nonce}{self.header.nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] !=  "0000"
        
