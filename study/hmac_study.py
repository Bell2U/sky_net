from Crypto.Hash import HMAC
from Crypto.Hash import SHA256


pkey = b'abcdefg'
key = SHA256.new(pkey).digest()     # bytes
msg = b'This is a hundred percent original message.'     # bytes
# print(key)
# print(msg)

hobj = HMAC.new(key, msg)
h = hobj.digest()
# print(h)
# print(len(h))

# combine the msg and HMAC.
def combine():
    combined = msg + h
    print(msg, h, combined, sep='\n')
# combine()

# split the combined message.
def split_():
    combined = msg + h
    sp_msg = combined[:-16]
    sp_hmac = combined[-16:]
    print(sp_msg, sp_hmac, sep='\n')
split_()
