import magic
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# Configuration - encryption key stored in a configuration file
from ..config import ENCRYPTION_KEY

def decrypt_image(iv: bytes, encrypted_data: bytes, encryption_key: bytes) -> str:
    """
    Decrypts the encrypted image data using AES decryption.

    Args:
        iv (bytes): The initialization vector (IV) used for encryption.
        encrypted_data (bytes): The encrypted image data.
        encryption_key (bytes): The encryption key.

    Returns:
        str: The decrypted image data encoded as a Base64 string.
    """
    try:
        # Create AES cipher object in CBC mode with the provided key and IV
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)

        # Decrypt the encrypted image data
        decrypted_data = cipher.decrypt(encrypted_data)

        # Unpad the decrypted data
        unpadded_data = unpad(decrypted_data, AES.block_size)

        # Encode the decrypted data as Base64 string
        base64_encoded_data = base64.b64encode(unpadded_data).decode('utf-8')

        return base64_encoded_data
    except Exception as e:
        print("Error decrypting image data:", e)
        return None

def encrypt_image(file_storage, encryption_key: bytes):
    """
    Encrypts the image data using AES encryption.

    Args:
        file_storage: The FileStorage object containing the image data.
        encryption_key (bytes): The encryption key.

    Returns:
        tuple: Tuple containing IV (Initialization vector) and encrypted image data.
    """
    try:
        # Read the image data from the FileStorage object
        image_data = file_storage.read()

        # Generate a random IV for encryption
        iv = get_random_bytes(16)  # 128-bit IV

        # Create AES cipher object in CBC mode with the provided key and IV
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)

        # Pad the image data to match the block size of AES
        padded_image_data = pad(image_data, AES.block_size)

        # Encrypt the padded image data
        encrypted_data = cipher.encrypt(padded_image_data)

        return iv, encrypted_data
    except Exception as e:
        print("Error encrypting image data:", e)
        return None, None

def validate_image(file):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg', 'image/gif'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 # 2 MB

    # Check if file has a filename
    if file.filename == '':
        return False, 'No selected file', ''

    # Check file extension
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
        return False, 'Invalid file extension', ''

    # Check MIME type
    mime_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    if mime_type not in ALLOWED_MIME_TYPES:
        return False, 'Invalid MIME type', mime_type

    # Check file size
    if len(file.read()) > MAX_CONTENT_LENGTH:
        return False, 'File size exceeds maximum allowed', mime_type

    # Reset file pointer
    file.seek(0)

    return True, 'Validation successful', mime_type
