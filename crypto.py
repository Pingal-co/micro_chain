import hashlib, base64
# hash functions in hashlib module: md5, sha1, sha224, sha256, sha384, sha512
# fastecdsa
from fastecdsa import keys, curve, ecdsa
from struct import pack, unpack
# base58
import base58

from utils import *


def compute_block_hash(block):
    """
    Creates a SHA-256 hash of a Block
    :param block: <dict> Block
    :return: <str>
    """
    # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
    hashed_str = hash(block, algo=hashlib.sha256, order=True)
    return base64.b64encode(hashed_str)

def verify_block_hash(self, block):
    pass

def gen_keypair(curve=curve.secp256k1):
    private_key, public_key = keys.gen_keypair(curve)
    public_key_tuple = (public_key.x, public_key.y)
    return (private_key, public_key_tuple)

def gen_private_key(curve=curve.secp256k1):
    # generate a private key for curve secp256k1 (bitcoin curve)
    return keys.gen_private_key(curve)

def get_public_key(private_key, curve=curve.secp256k1):
    # get the public key corresponding to the private key we just generated
    pk = keys.get_public_key(private_key, curve) 
    return (public_key.x, public_key.y)

def encode_pubkey(public_key):
    x_bytes = encode(public_key[0], 256, 32)
    y_bytes = encode(public_key[1], 256, 32)
    # the prepended 04 is used to signify that it's uncompressed
    # len(pk) == 65 ; length of public key is 65 (1+32+32)  
    return b'\x04' + x_bytes + y_bytes

def decode_pubkey(public_key):
    return (decode(public_key[1:33], 256), decode(public_key[33:65], 256))

def encode_privkey(private_key):
    return encode(private_key, 256, 32)

def decode_privkey(private_key):
    return decode(private_key, 32, 256)

def pubkey_to_address(public_key, network_id="01"):
    """
    # version of the bitcoin address, known has the Public Key Hash 
    # https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
        x,y = keys.public_key()
        address(x,y) = addrHash(string(x) <> string(y))
        addrHash(n) = sha256(sha256(ripemd160(sha256(n))))

    """
    # this returns the concatenated x and y coordinates for the supplied private address
    pk = uncompressed_public_key(public_key)
    address = hashlib.sha256(pk).digest()
    public_address = hashlib.new('ripemd160', address).digest()
    #h.update(address)
   # public_address = h.digest()
    # main_network: 00 ; test_network: 01
    version = int_to_bytes(int(network_id))
    checksum = hashlib.sha256(hashlib.sha256(version + public_address).digest()).digest()[:4]
    payload = version + public_address + checksum
 
    return base58.b58encode(payload)


def sign(msg, private_key):        
    #msg = "a message to sign via ECDSA"  # some message
    # standard signature, returns two integers
    private_key = decode_privkey(private_key)
    r, s = ecdsa.sign(msg, private_key, hashfunc=hashlib.sha256, curve=curve.secp256k1)
    #encoding to pack the r and s components into single byte stream
    rb, sb = encode(r, 256), encode(s, 256)
    signature = base64.b64encode(b'\x00'*(32-len(rb))+rb+b'\x00'*(32-len(sb))+sb)
    return signature

def verify_sign(msg, public_key, signature)
    bytez = base64.b64decode(signature)
    pub = decode_pubkey(public_key)
    
    r,s = decode(bytez[:32], 256), decode(bytez[32:], 256)
    # should return True as the signature we just generated is valid.
    valid = ecdsa.verify((r, s), msg, pub, hashfunc=hashlib.sha256, curve=curve.secp256k1)
    return valid

def hash(self, data, algo=hashlib.sha256, order=True):
    # serialize data as Ordered dict. Order is important.
    data_string = json.dumps(data, sort_keys=order).encode()
    return algo(block_string).hexdigest()

      
"""
# 58 character alphabet used
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
Gets a Base58Check string
See https://en.bitcoin.it/wiki/Base58Check_encoding
 
def base58_encode(version, public_address):
   version = bytes.fromhex(version)
    checksum = hashlib.sha256(hashlib.sha256(version + public_address).digest()).digest()[:4]
    payload = version + public_address + checksum
    
    result = int.from_bytes(payload, byteorder="big")
    
    # count the leading 0s
    padding = len(payload) - len(payload.lstrip(b'\0'))
    encoded = []

    while result != 0:
        result, remainder = divmod(result, 58)
        encoded.append(BASE58_ALPHABET[remainder])

    return padding*"1" + "".join(encoded)[::-1]
"""