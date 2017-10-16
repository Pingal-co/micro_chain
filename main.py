"""
Endpoints:

/address : View the address of the current node (derived from the nodes public key)

/blocks :  View the blocks on the block chain, including their transactions.

/mempool : View the current collected transactions that have not yet been included in a
block on the network.

/ledger : View the current state of the ledger, representative of all the transactions
of all the blocks applied in order to result in a cumulative ledger state.

/addBlock : Attempt to mine a block containing the transactions currently in the node's mempool.
This will fail if there are no transactions in the mempool. 

/transfer/:toAddress/:amount
Issues a `Transfer` transaction to the network, transferring the specified 
`amount` of tokens from this user | node's account to another user | node's account 
designated by `toAddress`. If you try to transfer more tokens than you
have, the transaction will be rejected during the block mining process and
purged from all nodes' mem-pools.
"""

class PeerNetwork(object):
    def __init__(self, peers=[]):
        self.peers = peers

    def add_peer(self, host, port):
        node_id = len(self.peers)
        node = peerNode(host, port, node_id)
        node.start()         
        self.peers.append(node)

    def remove_peer(self, host, port):
        self.peers = self.peers.filter(lambda p: p.host != host and p.port != port)

