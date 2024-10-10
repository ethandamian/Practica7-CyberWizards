from cryptography.fernet import Fernet
import os 

def load():
    return open('key.key', 'rb').read()

def decrypt(files,key):
    fernet = Fernet(key)
    for file in files:
        with open(file, 'rb') as f:
            data = f.read()
        decrypted = fernet.decrypt(data)
        with open(file, 'wb') as f:
            f.write(decrypted)

if __name__ == '__main__':
    key = load()
    path_to_decrypt = './TestFiles'
    

    os.remove(path_to_decrypt + './README.txt')
    os.remove('./key.key') # Maybe we don't want to delete the key, idk

    items = os.listdir(path_to_decrypt)
    full_path = [path_to_decrypt + '/' + item for item in items]

    decrypt(full_path, key)