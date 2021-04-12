from Crypto.Cipher import AES
from Crypto.Random import random
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16     # bytes, any interger multiple of 16 is fine

randombits = random.getrandbits(32)
key = SHA256.new(str(randombits).encode('ascii')).digest()
# print(len(key))

msg = b'This is the secret message'
padded_msg = pad(msg, BLOCK_SIZE)

cipher = AES.new(key, AES.MODE_ECB)
encrypted_message = cipher.encrypt(padded_msg)
# decrypted_padded_msg = cipher.decrypt(encrypted_message)
# decrypted_message = unpad(decrypted_padded_msg, BLOCK_SIZE)

another_cipher = AES.new(key, AES.MODE_ECB)
decrypted_padded_msg = another_cipher.decrypt(encrypted_message)
decrypted_message = unpad(decrypted_padded_msg, BLOCK_SIZE)

# print(encrypted_message)
# print(decrypted_message)
# print(decrypted_message.decode('ascii'))
# print(type(decrypted_message.decode('ascii')))


# a_choice = random.choice([1, 2, 3, 4, 5])
# print(a_choice)
