
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Clé et sel stockés en variables d'environnement pour la sécurité
KEY = os.getenv('ENCRYPTION_KEY')
SALT = os.getenv('ENCRYPTION_SALT')

if not KEY or not SALT:
    raise ValueError("Les variables d'environnement ENCRYPTION_KEY et ENCRYPTION_SALT doivent être définies.")

def generate_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def encrypt(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode()

# Example usage
if __name__ == "__main__":
    password = "AppWebAmendis123@@"
    salt = os.urandom(16)
    key = generate_key(password, salt)
    encrypted_data = encrypt("Sensitive Data", key)
    decrypted_data = decrypt(encrypted_data, key)
    print("Encrypted:", encrypted_data)
    print("Decrypted:", decrypted_data)
