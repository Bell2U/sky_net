import struct
from typing import Tuple

from dh import create_dh_key, calculate_dh_secret
from .xor import XOR
from Crypto.Hash import HMAC


class StealthConn(object):
    def __init__(self, conn, client=False, server=False, verbose=False):
        self.conn = conn
        self.cipher = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.session_id = None
        self.initiate_session()

    def initiate_session(self):
        # Perform the initial connection handshake for agreeing on a shared secret 

        ### TODO: Your code here!
        # This can be broken into code run just on the server or just on the clientasdsad
        if self.server or self.client:
            my_public_key, my_private_key = create_dh_key()
            # Send them our public key
            self.send(bytes(str(my_public_key), "ascii"))
            # Receive their public key
            their_public_key = int(self.recv())
            # Obtain our shared secret
            shared_hash = calculate_dh_secret(their_public_key, my_private_key)
            print("Shared hash: {}".format(shared_hash.hex()))

            # Default XOR algorithm can only take a key of length 32
            self.cipher = XOR.new(shared_hash[:32])      # I need 32 bits key instead of 4!

            # generate a session ID by shared hash, to prevent replay attack.
            self.session_id = shared_hash[-10:]

    def send(self, data: bytes):
        if self.cipher:
            msg = self.session_id + data
            hmac_data = self.hmac(msg)
            encrypted_data = self.cipher.encrypt(hmac_data)
            if self.verbose:
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = data

        # Encode the data's length into an unsigned two byte int ('H')
        pkt_len = struct.pack('H', len(encrypted_data))
        self.conn.sendall(pkt_len)
        self.conn.sendall(encrypted_data)

    def recv(self):
        # Decode the data's length from an unsigned two byte int ('H')
        pkt_len_packed = self.conn.recv(struct.calcsize('H'))
        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]

        encrypted_data = self.conn.recv(pkt_len)
        if self.cipher:
            hmac_data = self.cipher.decrypt(encrypted_data)

            # integrity check(MAC)
            integrity, msg = self.hmac_check(hmac_data)
            if integrity:

                # replay attack check (check the sesssion ID)
                # session_id is the first 10 bits of the msg
                session_id = msg[:10]
                data = msg[10:]
                if session_id == self.session_id:

                    # display details?
                    if self.verbose:
                        print("Receiving packet of length {}".format(pkt_len))
                        print("Encrypted data: {}".format(repr(encrypted_data)))
                        print("Original data: {}".format(data))
                else:
                    print('[Warning] Replay attack detected')
                    data = encrypted_data
            else:
                print('[Warning] MAC check failed, received data has been modified.')
                data = encrypted_data
        else:
            data = encrypted_data

        return data

    def close(self):
        self.conn.close()

    def hmac(self, message: bytes) -> bytes:
        # generates a 16 bits MAC, and append it to the original message.
        K = self.cipher.key
        hmac_ = HMAC.new(K, message).digest()
        return message + hmac_

    def hmac_check(self, h_msg: bytes) -> Tuple[bool, bytes]:
        # check the integrity base on the key, and obtain the original message.
        # MAC is a 16-bits-long bytes string appending to the original message.
        sp_msg = h_msg[:-16]
        if h_msg == self.hmac(sp_msg):
            return (True, sp_msg)
        else:
            return (False, sp_msg)

