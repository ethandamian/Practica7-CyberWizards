from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
import os

def load():
    return open('key.key', 'rb').read()  # Cargar la clave desde un archivo

def load_private_key(private_key_path='private_key.pem'):
    # Cargar la llave privada RSA desde el archivo
    with open(private_key_path, 'rb') as priv_file:
        private_key = RSA.import_key(priv_file.read())
    return private_key

def decrypt_aes_key_with_private_key(encrypted_key_path='key.key.enc', private_key=None):
    # Cargar la clave AES cifrada desde el archivo
    with open(encrypted_key_path, 'rb') as enc_file:
        encrypted_key = enc_file.read()

    # Crear un descifrador RSA usando PKCS1_OAEP
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_key = cipher_rsa.decrypt(encrypted_key)
    return decrypted_key

def save_decrypted_aes_key(decrypted_key, output_path='key.key'):
    # Guardar la clave AES descifrada en un archivo
    with open(output_path, 'wb') as key_file:
        key_file.write(decrypted_key)
    print(f"Clave AES descifrada guardada en '{output_path}'.")

def decrypt(files, key):
    for file in files:
        with open(file, 'rb') as f:
            # Leer el IV (primeros 16 bytes) y el contenido cifrado
            iv = f.read(16)  # Leer el IV
            encrypted_data = f.read()  # Leer el resto de los datos cifrados
        
        # Crear un objeto de cifrado AES en modo CBC con el IV
        cipher = AES.new(key, AES.MODE_CBC, iv)  
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)  # Desencriptar y quitar el padding

        with open(file, 'wb') as f:
            f.write(decrypted_data)  # Sobrescribir el archivo con datos desencriptados

if __name__ == '__main__':
    # path_to_decrypt = './TestFiles'  # Cambia esto a la ruta deseada
    documents_path = os.path.join(os.environ["USERPROFILE"], "Documents")

     # Cargar la llave privada
    private_key = load_private_key('private_key.pem')

    # Descifrar la clave AES
    decrypted_aes_key = decrypt_aes_key_with_private_key(private_key=private_key)

    # Guardar la clave AES descifrada
    save_decrypted_aes_key(decrypted_aes_key)

     # Eliminar llave cifrada
    if os.path.exists("key.key.enc"):
        os.remove("key.key.enc")

    key = load()  # Cargar la clave

    # Eliminar el archivo README si existe
    readme_path = os.path.join(documents_path, 'README.txt')
    if os.path.exists(readme_path):
        os.remove(readme_path)

    # Cargar la lista de archivos para desencriptar
    items = os.listdir(documents_path)
    full_path = [os.path.join(documents_path, item) for item in items]

    # Desencriptar archivos
    decrypt(full_path, key)
