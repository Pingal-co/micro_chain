# binascii
import binascii
import os
import hashlib
from datetime import datetime

# Base switching
code_strings = {
    2: '01',
    10: '0123456789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    58: '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz',
    256: ''.join([chr(x) for x in range(256)])
}


def hash160(string):
    return safe_hexlify(bin_hash160(string))


def bin_sha256(string):
    binary_data = string if isinstance(string, bytes) else bytes(string, 'utf-8')
    return hashlib.sha256(binary_data).digest()

def sha256(string):
    return bytes_to_hex_string(bin_sha256(string))

def bin_ripemd160(string):
    digest = hashlib.new('ripemd160', string).digest()
    return digest

def ripemd160(string):
    return safe_hexlify(bin_ripemd160(string))

def bin_dbl_sha256(s):
        bytes_to_hash = from_string_to_bytes(s)
        return hashlib.sha256(hashlib.sha256(bytes_to_hash).digest()).digest()

def dbl_sha256(string):
    return safe_hexlify(bin_dbl_sha256(string))

def bin_ripemd_sha256(s):
        return bin_ripemd160(bin_dbl_sha256(s))


def lpad(msg, symbol, length):
        if len(msg) >= length:
            return msg
        return symbol * (length - len(msg)) + msg

def get_code_string(base):
    if base in code_strings:
        return code_strings[base]
    else:
        raise ValueError("Invalid base!")

def changebase(string, frm, to, minlen=0):
        if frm == to:
            return lpad(string, get_code_string(frm)[0], minlen)
        return encode(decode(string, frm), to, minlen)

def bin_to_b58check(inp, magicbyte=0):
        if magicbyte == 0:
            inp = '\x00' + inp
        while magicbyte > 0:
            inp = chr(int(magicbyte % 256)) + inp
            magicbyte //= 256
        leadingzbytes = len(re.match('^\x00*', inp).group(0))
        checksum = bin_dbl_sha256(inp)[:4]
        return '1' * leadingzbytes + changebase(inp+checksum, 256, 58)

def safe_hexlify(a):
    return binascii.hexlify(a) 

def bytes_to_hex_string(b):
        return b.encode('hex')

def safe_from_hex(s):
    return s.decode('hex')

def from_int_to_bytes(a):
    return str(a)

def from_int_to_byte(a):
    return chr(a)

def from_byte_to_int(a):
    return ord(a)

def from_bytes_to_string(s):
    return s

def from_string_to_bytes(a):
    return a

def int_to_bytes(x):
    bs = ''

    while x:
        bs = pack('=B', (0xff & x)) + bs
        x >>= 8

    return bs

def encode(val, base, minlen=0):
        base, minlen = int(base), int(minlen)
        code_string = get_code_string(base)
        result = ""
        while val > 0:
            result = code_string[val % base] + result
            val //= base
        return code_string[0] * max(minlen - len(result), 0) + result

def decode(string, base):
    base = int(base)
    code_string = get_code_string(base)
    result = 0
    if base == 16:
        string = string.lower()
    while len(string) > 0:
        result *= base
        result += code_string.find(string[0])
        string = string[1:]
    return result

def random_string(x):
    return os.urandom(x)

def num_to_var_int(x):
    # variable length encoding depending upon the number
    x = int(x)
    if x < 253: return from_int_to_byte(x)
    elif x < 65536: return from_int_to_byte(253)+encode(x, 256, 2)[::-1]
    elif x < 4294967296: return from_int_to_byte(254) + encode(x, 256, 4)[::-1]
    else: return from_int_to_byte(255) + encode(x, 256, 8)[::-1]

def is_sha256(s):
    return len(s) == 64

def is_ripemd160(s):
    return len(s) == 40