import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import random
from Crypto.Hash import SHA256

# generate the AES key for the server
randombits = random.getrandbits(32)
key = SHA256.new(str(randombits).encode('ascii')).digest()
# define the block size for AES block cipher
PAD_BLOCK_SIZE = 16

# Instead of storing files on disk,
# we'll save them in memory for simplicity
filestore = {}
# Valuable data to be sent to the botmaster
valuables = []

###

def save_valuable(data):
    valuables.append(data)

def encrypt_for_master(data: bytes) -> bytes:
    # Encrypt the file so it can only be read by the bot master
    
    # encrypt the data by using AES method
    # pad the data
    paded_data = pad(data, PAD_BLOCK_SIZE)
    # encrption
    cipher = AES.new(key, AES.MODE_ECB)
    data = cipher.encrypt(paded_data)

    return data

def decrypt_for_master(encrypted_data: bytes) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    paded_decrypted_data = cipher.decrypt(encrypted_data)
    decrypted_data = unpad(paded_decrypted_data, PAD_BLOCK_SIZE).decode('ascii')
    return decrypted_data

def upload_valuables_to_pastebot(fn):
    # Encrypt the valuables so only the bot master can read them
    valuable_data = "\r\n".join(valuables)
    print(valuable_data)
    valuable_data = bytes(valuable_data, "ascii")
    encrypted_master = encrypt_for_master(valuable_data)

    # "Upload" it to pastebot (i.e. save in pastebot folder)
    f = open(os.path.join("pastebot.net", fn), "wb")
    f.write(encrypted_master)
    f.close()

    print("Saved valuables to pastebot.net/%s for the botnet master" % fn)

###

def verify_file(f):
    # Verify the file was sent by the bot master
    # TODO: For Part 2, you'll use public key crypto here
    # Naive verification by ensuring the first line has the "passkey"
    lines = f.split(bytes("\r\n", "ascii"), 1)
    first_line = lines[0]
    if first_line == bytes("Caesar", "ascii"):
        return True
    return False

def process_file(fn, f):
    if verify_file(f):
        # If it was, store it unmodified
        # (so it can be sent to other bots)
        # Decrypt and run the file
        filestore[fn] = f
        print("Stored the received file as %s" % fn)
    else:
        print("The file has not been signed by the botnet master")

def download_from_pastebot(fn):
    # "Download" the file from pastebot.net
    # (i.e. pretend we are and grab it from disk)
    # Open the file as bytes and load into memory
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        return
    # f = open(os.path.join("pastebot.net", fn), "rb").read()
    with open(os.path.join("pastebot.net", fn), "rb") as F:
        f = F.read()
        process_file(fn, f)

def p2p_download_file(sconn):
    # Download the file from the other bot
    fn = str(sconn.recv(), "ascii")
    f = sconn.recv()
    print("Receiving %s via P2P" % fn)
    process_file(fn, f)

###

def p2p_upload_file(sconn, fn):
    # Grab the file and upload it to the other bot
    # You don't need to encrypt it only files signed
    # by the botnet master should be accepted
    # (and your bot shouldn't be able to sign like that!)
    if fn not in filestore:
        print("That file doesn't exist in the botnet's filestore")
        return
    print("Sending %s via P2P" % fn)
    sconn.send(bytes(fn, 'ascii'))
    sconn.send(bytes(filestore[fn]))

def run_file(f):
    # If the file can be run,
    # run the commands
    pass
