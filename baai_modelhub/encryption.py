import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from . import RSA
import os




# ------------------------生成密钥对------------------------
def create_rsa_pair(is_save=False):
    '''
    创建rsa公钥私钥对
    :param is_save: default:False
    :return: public_key, private_key
    '''
    f = RSA.generate(2048)
    private_key = f.exportKey("PEM")  # 生成私钥
    public_key = f.publickey().exportKey()  # 生成公钥
    if is_save:
        with open("crypto_private_key.pem", "wb") as f:
            f.write(private_key)
        with open("crypto_public_key.pem", "wb") as f:
            f.write(public_key)
    return public_key, private_key


def read_public_key(file_path="/root/.ssh/id_rsa.pub") -> bytes:

    with open(file_path, "rb") as x:
        b = x.read()
        return b


def read_private_key(file_path="/root/.ssh/id_rsa") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b


# ------------------------加密------------------------
def encryption(text: str, private_key: bytes):
    # 字符串指定编码（转为bytes）
    text = text.encode('utf-8')
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64


# ------------------------解密------------------------
def decryption(text_encrypted_base64: str, public_key: bytes):
    # 字符串指定编码（转为bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64解码
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
    cipher_private = PKCS1_v1_5.new(RSA.importKey(public_key))
    # 解密（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
    text_decrypted = text_decrypted.decode()
    return text_decrypted

class BAAIUserClient():
    def __init__(self,
                 user_name='default_name'):
        self.user_name=user_name
        self.user_path = '/tmp/.cache/baai_modelhub/user'
        self.cache_path = '/tmp/.cache/baai_modelhub/'

        if self.user_name!='default_name':
            with open(self.user_path, "w") as x:
                x.write(self.user_name)
                x.write('\n')

    def obtain_username(self,):
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        if 1:
            with open(self.user_path, "r") as x:
                return x.read().strip('\n')
            return self.user_name
        else:
            print('Please type your username of baai.ac.cn:')
            user_name=input()

            if len(user_name.strip('\n') )<1:
                user_name=self.user_name
            with open(self.user_path, "w") as x:
                x.write(self.user_name)
                x.write('\n')
            return self.user_name

    def clear_cache(self):
        if os.path.exists(self.user_path):
            os.remove(self.user_path)

    def login(self,):
        print('Please type your username of baai.ac.cn:')
        user_name = input()
        self.user_name=user_name
        with open(self.user_path, "w") as x:
            x.write(self.user_name)
            x.write('\n')

    def passward_login(self,):
        print('Please type your username of baai.ac.cn:')
        user_name = input()
        print('Please type the passward:')
        passward =input()
        print('Please type the verification code of FreeOTP:')
        passward = input()
        token=''
        return token



if __name__ == '__main__':
    user_client=BAAIUserClient(user_name='wangguojim1')
    # user_client.clear_cache()
    public_key = read_public_key()
    private_key = read_private_key()
    # 加密
    text =user_client.obtain_username()
    text_encrypted_base64 = encryption(text, private_key)
    print('密文：', text_encrypted_base64)
    # 解密
    text_decrypted = decryption(text_encrypted_base64, public_key)
    print('明文：', text_decrypted)

