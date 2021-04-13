from Crypto.Util import strxor
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

__all__ = ("XOR",)


class XOR:
    __slots__ = ("key", "_keylen", "_last_pos")

    block_size = 1
    pad_block_size = 16

    def __init__(self, key: bytes) -> None:
        assert 0 < len(key) <= 32, "XOR key must be no longer than 32 bytes"
        self.key = key
        self._last_pos = 0

    @classmethod
    def new(cls, key: bytes) -> "XOR":
        return cls(key)

    def encrypt(self, plaintext: bytes) -> bytes:
        # XOR cipher
        key = rotate(self.key, self._last_pos)
        keylen = len(key)
        pt_len = len(plaintext)
        key *= pt_len // keylen + 1
        key = key[:pt_len]
        self._last_pos = (self._last_pos + pt_len) % keylen
        xor_encrypted = strxor.strxor(plaintext, key)

        # AES cipher
        padded_msg = pad(xor_encrypted, XOR.pad_block_size)
        AES_instance = AES.new(self.key, AES.MODE_ECB)
        return AES_instance.encrypt(padded_msg)

    def decrypt(self, ciphertext: bytes) -> bytes:
        # decrypt AES by self.key
        AES_instance = AES.new(self.key, AES.MODE_ECB)
        decrypted_paded = AES_instance.decrypt(ciphertext)
        aes_decrypted = unpad(decrypted_paded, XOR.pad_block_size)

        # decrypt XOR
        key = rotate(self.key, self._last_pos)
        keylen = len(key)
        pt_len = len(aes_decrypted)
        key *= pt_len // keylen + 1
        key = key[:pt_len]
        self._last_pos = (self._last_pos + pt_len) % keylen
        return strxor.strxor(aes_decrypted, key)


def rotate(s: bytes, n: int) -> bytes:
    return s[n:] + s[:n]
