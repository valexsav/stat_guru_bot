import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC

from constants import MASTER_KEY


def generate_key(salt: bytes) -> bytes:
    hmac = HMAC(MASTER_KEY, hashes.SHA256(), backend=default_backend())
    hmac.update(salt)
    return hmac.finalize()


def encrypt_data(plaintext: str) -> bytes:
    salt = os.urandom(16)
    iv = os.urandom(16)
    key = generate_key(salt)

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = bytes(encryptor.update(plaintext.encode()) + encryptor.finalize())

    return salt + iv + ciphertext + encryptor.tag


def decrypt_data(ciphertext: bytes) -> str:
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    tag = ciphertext[-16:]
    encrypted_data = ciphertext[32:-16]

    key = generate_key(salt)

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        return decrypted_data.decode()
    except Exception as e:
        raise ValueError("Decryption failed") from e
