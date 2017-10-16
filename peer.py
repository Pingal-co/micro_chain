class Node(object):
    def __init__(self, host, port, node_id):
        """
        NodeState = NodeState
        { nodeConfig   :: Peer                   -- ^ P2P info (rpc port, p2p port)
        , nodeChain    :: MVar Block.Blockchain  -- ^ In-memory Blockchain
        , nodeKeys     :: KeyPair                -- ^ Node key pair
        , nodeSender   :: MsgSender              -- ^ Function to broadcast a P2P message
        , nodeReceiver :: MsgReceiver            -- ^ The source of network messages
        , nodeLedger   :: MVar Ledger.Ledger     -- ^ In-memory ledger state
        , nodeMemPool  :: MVar MemPool.MemPool   -- ^ Mempool to collect transactions
        } 
        """
        self.node_id = node_id
        self.host_ip = host
        self.port = port
        self.node_state() 

    def start(self):
        # connect and run the node
        self.update_node_state()
        # start the service

    def stop(self):
        # disconnect the node
        """
        - save the blockchain in local db
        - stop the service
        """
        pass

    def node_state(self):
        self.ledger = self.get_ledger()
        self.blockchain = self.get_blockchain()
        self.mempool = self.get_mempool()
        self.receiver = self.listen()


    def update_node_state(self):
        """
        # run consensus over neighbors, 
        # choose the chain and the ledger from the winner/master node
        """
        self.blockchain.update()

    def get_blockchain(self):
        return self.blockchain or Blockchain()

    def get_ledger(self):
        return self.ledger or Ledger()

    def get_mempool(self):
        return self.mempool or MemoryPool()

    def add_transaction(self, tx):
        self.mempool.add_transaction(tx)

    def broadcast(self, msg):
        return NodeMessage(msg).broadcast()

    def listen(self):
        # subscribe & listen to the web socket
        pass

    def mine():
        # /mine
        last_block = self.blockchain.last_block()
        last_proof = last_block.header.nonce
        proof = self.blockchain.consensus.proof_of_work(last_proof)

        # add a reward to find the proof
        self.add_transaction(Transaction(
                senderKey="0",
                recipient=node_identifier,
                amount=1,
                )
        )

        # add a block
        block = self.blockchain.new_block(Block(
            nonce = proof    
        ))

        # send message to others
        self.broadcast(block)


class NodeMessage(object):
    """
    data Msg 
    = QueryBlockMsg Int
    | BlockMsg Block
    | TransactionMsg Transaction
    """
    def __init__(self, msg):
        if isinstance(msg, int):
            self.msg = self.blockchain.find_block_by_index(msg)
        if isinstance(msg, Block):
            self.msg = Block
        if isinstance(msg, Transaction):
            self.msg = msg

    def broadcast():
        # serialize the msg and publish on web socket
        pass


