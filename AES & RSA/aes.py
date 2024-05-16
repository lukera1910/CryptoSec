from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_message(message, key):
    iv = b'1234567890123456' # Vetor de inicialização de 16 bytes
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()) # Objeto 'cipher' que será utilizado para criptografar
    encryptor = cipher.encryptor() # Objeto 'encryptor' a partir do 'cipher', que será usado para criptografar a mensagem
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize() # Criptografamos a mensagem convertida em bytes e concatenamos o resultado com IV
    return base64.b64encode(iv + ciphertext) # Retornamos o texto cifrado codificado em base64 para facilitar o envio pela rede

def decrypt_message(encrypted_message, key):
    encrypted_message = base64.b64decode(encrypted_message)
    iv = encrypted_message[:16]  # Obtém o IV do início da mensagem
    ciphertext = encrypted_message[16:]  # Obtém o texto cifrado
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend()) # Seguindo a mesma lógica da função de cima, só que para descriptografar
    decryptor = cipher.decryptor() 
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message

if __name__ == "__main__":
    password = "senha_super_secreta"
    salt = b'salt_aleatorio'
    message = input("Qual mensagem deseja enviar e criptografar? ")
    
    key = generate_key(password, salt)
    encrypted_message = encrypt_message(message, key)
    print("Mensagem criptografada:", encrypted_message)
    
    decrypted_message = decrypt_message(encrypted_message, key)
    print("Mensagem descriptografada:", decrypted_message.decode('utf-8'))