#!/usr/bin/python3
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, PKCS1_OAEP
import base64
from urllib import parse


def create_rsa_key(secret_code='penghaidong'):
    key = RSA.generate(1024)
    encrypted_key = key.exportKey(passphrase=secret_code, pkcs=8,
                                  protection="scryptAndAES128-CBC")
    with open("private_key.bin", "wb") as f:
        f.write(encrypted_key)     # 将私钥存入文件中

    with open("public_key.pem", "wb") as f:
        f.write(key.publickey().exportKey())   # 将公钥存入文件中


# 解密web数据
def decrypt(en_data, secret_code="penghaidong"):
    # 读取密钥
    data = parse.unquote(en_data)
    data = base64.b64decode(data)
    private_key = RSA.import_key(open("private_key.bin").read(), passphrase=secret_code)
    cipher_rsa = PKCS1_v1_5.new(private_key)
    data = cipher_rsa.decrypt(data, None)   # 解密
    return data

# 界面节点上传的数据
def decrypt_upload_data(en_data, secret_code="penghaidong"):
    data = base64.b64decode(en_data)
    private_key = RSA.import_key(open("private_key.bin").read(), passphrase=secret_code)
    cipher_rsa = PKCS1_v1_5.new(private_key)
    data = cipher_rsa.decrypt(data, None)   # 解密
    return data

# 加密
def encrypt(data):
    pub = RSA.import_key(open("public_key.pem").read())
    cipher_rsa = PKCS1_v1_5.new(pub)
    data = base64.b64encode(cipher_rsa.encrypt(data))
    return data

def get_public_key():
    return RSA.import_key(open("public_key.pem").read()).export_key().decode().replace("\n", "")


def get_priv_key():
    return RSA.import_key(open("private_key.bin").read(), passphrase="123456").export_key().decode()


def _get_public_key():
    return RSA.import_key(open("public_key.pem").read()).export_key().decode()


if __name__ == '__main__':
    print("Module Name:RSA")
    print("Function:RSA decode/encode")
