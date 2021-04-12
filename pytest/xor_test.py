import os, sys, inspect
current_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(current_dir)
sys.path.append('../')

from lib.xor import XOR, rotate
from Crypto.Util import strxor

def encrypt_test():
    key = b'2A57'
    plain_text = b'I love red'
    xorr = XOR(key)
    ciphertext = xorr.encrypt(plain_text)
    print(ciphertext)
    decrypt_text = xorr.decrypt(ciphertext)
    print(decrypt_text.decode('ascii'))
# encrypt_test()

def xor_test():
    key = b'abcd'
    plain_tesxt = b'1234'
    ciphertext = strxor.strxor(key, plain_tesxt)
    decrypted_text = strxor.strxor(key, ciphertext)
    assert plain_tesxt == decrypted_text
xor_test()

def rotate_test():
    key = b'wsad'
    pos = 0
    assert rotate(key, pos) == b'wsad'
    pos = 2
    assert rotate(key, pos) == b'adws'
rotate_test()
