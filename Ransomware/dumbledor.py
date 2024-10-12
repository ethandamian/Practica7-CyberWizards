from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

def load():
    return open('key.key', 'rb').read()  # Cargar la clave desde un archivo

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
    key = load()  # Cargar la clave
    path_to_decrypt = './TestFiles'  # Cambia esto a la ruta deseada

    # Eliminar el archivo README si existe
    readme_path = os.path.join(path_to_decrypt, 'README.txt')
    if os.path.exists(readme_path):
        os.remove(readme_path)

    # Cargar la lista de archivos para desencriptar
    items = os.listdir(path_to_decrypt)
    full_path = [os.path.join(path_to_decrypt, item) for item in items]

    # Desencriptar archivos
    decrypt(full_path, key)
