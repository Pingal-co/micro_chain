import hashlib
import json
from time import time
from uuid import uuid4

import requests


class Blockchain(object):
    def __init__(self):
        # store incoming transactions in memory
        self.mempool = MemoryPool()
        # actual blockchain in memory
        self.blocks = []
        # peer network
        self.peers = set()
        # consensus algorithm
        self.consensus = Consensus()

        # create the genesis block
        self.new_block(nonce=100, previous_hash=1)

    
    def new_block(self, nonce, previous_hash):
        """
        creates a new block in the blockchain
        """
        block = Block(
                index = len(self.blocks) + 1,
                timestamp = time(),
                transactions = self.mempool,
                nonce = nonce,
                previous_hash = previous_hash or self.hash(self.blocks[-1]),
                miner_pubkey = "",
                miner_signature = "",
                merkle_root = ""
        })
        
        self.blocks.append(block)
        
        # reset the current list of transactions
        self.mempool.remove_transactions(block)


    def last_block(self):
        return self.blocks[-1]


    def valid_chain(self, chain):
        """
        validate a given blockchain
        """
        prev_block = blocks[0]
        current_block_index = 1

        while current_block_index < len(blocks):
            block = blocks[current_block_index]
            if not block.validate_block(prev_block):
                return False
            prev_block = block
            current_block_index +=1

    def resolve_conflicts(self, prev_block):
        """
            resolve conflicts: longest chain among the neighbors/peers wins
        """
        pass

    def update(self, block):
        if not isinstance(block, Block):
            block=Block(block)

        # genesis block is not instantiated
        if len(self.blockchain)<1:
            block.add_genesis_block()

        # verify block before adding
        if block.validate_block():
                self.blocks.append(block)
        else:                
            # log error
            print "block is not valid"




