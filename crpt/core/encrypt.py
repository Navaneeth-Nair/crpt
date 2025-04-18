"""
Encryption utilities for GitHub Clone Crypt.
This module provides functions for encrypting and decrypting repository data.
"""

import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Default values
DEFAULT_KEY_FILE = ".crpt/encryption_key"
SALT_SIZE = 16
IV_SIZE = 16
KEY_SIZE = 32  # 256 bits for AES-256


def derive_key(password, salt, iterations=100000):
    """
    Derive a key from a password and salt using PBKDF2.
    
    Args:
        password (str): The password to derive the key from
        salt (bytes): The salt to use for key derivation
        iterations (int): Number of iterations for PBKDF2
        
    Returns:
        bytes: Derived key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_data(data, key):
    """
    Encrypt data using AES-256-CBC.
    
    Args:
        data (bytes): Data to encrypt
        key (bytes): Encryption key
        
    Returns:
        tuple: (encrypted_data, iv)
    """
    iv = os.urandom(IV_SIZE)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # PKCS#7 padding
    padding_length = 16 - (len(data) % 16)
    padded_data = data + bytes([padding_length]) * padding_length
    
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_data, iv


def decrypt_data(encrypted_data, key, iv):
    """
    Decrypt data using AES-256-CBC.
    
    Args:
        encrypted_data (bytes): Data to decrypt
        key (bytes): Encryption key
        iv (bytes): Initialization vector
        
    Returns:
        bytes: Decrypted data
    """
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Remove PKCS#7 padding
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]


def encrypt_file_content(content, password):
    """
    Encrypt file content using a password.
    
    Args:
        content (bytes): File content to encrypt
        password (str): Password for encryption
        
    Returns:
        bytes: Encrypted content with salt and IV prepended
    """
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    
    encrypted_data, iv = encrypt_data(content, key)
    
    # Format: salt + iv + encrypted_data
    return salt + iv + encrypted_data


def decrypt_file_content(encrypted_content, password):
    """
    Decrypt file content using a password.
    
    Args:
        encrypted_content (bytes): Encrypted file content
        password (str): Password for decryption
        
    Returns:
        bytes: Decrypted file content
    """
    salt = encrypted_content[:SALT_SIZE]
    iv = encrypted_content[SALT_SIZE:SALT_SIZE+IV_SIZE]
    encrypted_data = encrypted_content[SALT_SIZE+IV_SIZE:]
    
    key = derive_key(password, salt)
    
    return decrypt_data(encrypted_data, key, iv)


def get_or_create_encryption_key(password=None, key_file=DEFAULT_KEY_FILE):
    """
    Get or create an encryption key for the repository.
    
    Args:
        password (str, optional): Password for encryption
        key_file (str, optional): Path to key file
        
    Returns:
        bytes: Encryption key
    """
    # Use environment variable if available
    if not password:
        password = os.environ.get("CRPT_PASSWORD", "")
    
    # If still no password, check if key file exists
    if not password and os.path.exists(key_file):
        with open(key_file, "rb") as f:
            encoded_key = f.read()
            return base64.b64decode(encoded_key)
    
    # Otherwise generate and store a new key
    if not password:
        # Generate a random password if not provided
        password = base64.b64encode(os.urandom(16)).decode('utf-8')
    
    salt = os.urandom(SALT_SIZE)
    key = derive_key(password, salt)
    
    # Ensure directory exists
    key_dir = os.path.dirname(key_file)
    os.makedirs(key_dir, exist_ok=True)
    
    # Store encoded key
    with open(key_file, "wb") as f:
        encoded_key = base64.b64encode(key)
        f.write(encoded_key)
    
    return key