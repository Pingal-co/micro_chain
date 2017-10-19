"""
-- Blockchain 
An expression either evaluates to True or it fails. 
If failed, the transaction containing the scriptSig that provides the data input cannot be added to the blockchain 
(any block that contains that transaction will be rejected as invalid by full nodes). 
If it evaluates True and everything else about the transaction is correct, the transaction may be added to the blockchain.

-- If expression's only valid end state is “return True”, 
then things like Turing completeness are arguably useless extras

TO DO:
I must fix the builtin procedures and the serialization order to parse the incoming message.

"""

# map of constants and local variables
constants = {}
# map of functions
procedures = {}
# crypto decode: inputs are hashing using XYZ crypto algo
decoder = {}

############ SMART CONTRACTS ################


def equal_verify(s):
    second = s.pop(len(s) - 2)
    first = s.pop()
    # appends boolean on the stack
    s.append(second == first)
    # verify
    verify = s.pop() == True
    output(verify)

def check_sig(s):
    signature = s.pop(len(s) - 2)
    pub_key = s.pop()
    # now verify the signature using functions in crypto.py 
    verify = True
    output(verify)

def check_multisig(s):
    # m of n signatures must be valid
    parameters = s.pop()
    m = parameters[0]
    n = parameters[-1]
    nkeys = parameters[1:-1]
    # now verify the signature using functions in crypto.py 
    verify = True
    output(verify)

def escrow_with_timeout(s):
    pass

# A smart contract is just a stored procedure and anonymous function

### BOOLEAN LOGIC HANDLING ###
procedures["CMD_VERIFY"]    = lambda stack: stack.pop() == True
procedures["CMD_EQUAL"]    = lambda stack: stack.pop(len(stack) - 2) == stack.pop()
procedures["CMD_EQUALVERIFY"]    = lambda stack: equal_verify(stack)

### CRYPTO CMD ###
# The input is hashed using RIPEMD-160.
procedures["CMD_RIPEMD160"]    = lambda stack: stack.append( bin_ripemd160( stack.pop() ) )
procedures["CMD_SHA256"]    = lambda stack: stack.append( bin_shaa256( stack.pop() ) )
# The input is hashed twice: first with SHA-256 and then with RIPEMD-160
procedures["CMD_HASH160"]    = lambda stack: stack.append( bin_sha256_ripemd160( stack.pop() ) ) 
# The input is hashed two times with SHA-256.
procedures["CMD_HASH256"]    = lambda stack: stack.append( bin_dbl_sha256( stack.pop() ) ) 

### SIGNATURE###
procedures["CMD_CHECKSIG"]    = lambda stack: check_sig(stack)
procedures["CMD_CHECKMULTISIG"]    = lambda stack: check_multisig(stack)

### CONTRACTS ###
# escrow or contract_expiry_check: verify if top stack item > transaction's nLockTime
# https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki
procedures["CMD_LOCKTIMEVERIFY"]    = lambda stack: check_sig(stack)
# escrow with timeout: https://github.com/bitcoin/bips/blob/master/bip-0112.mediawiki#Motivation
procedures["CMD_ESCROWTIMEOUT"]    = lambda stack: escrow_with_timeout(stack)
