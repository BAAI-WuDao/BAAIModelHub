import base64
import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from . import RSA
from Crypto.PublicKey import RSA as OldRSA




# ------------------------生成密钥对------------------------
def create_rsa_pair(is_save=False):
    '''
    创建rsa公钥私钥对
    :param is_save: default:False
    :return: public_key, private_key
    '''
    f = OldRSA.generate(2048)
    private_key = f.exportKey("PEM")  # 生成私钥
    public_key = f.publickey().exportKey()  # 生成公钥
    return public_key, private_key


def read_public_key(file_path="/root/.ssh/id_rsa.pub") -> bytes:

    with open(file_path, "rb") as x:
        b = x.read()
        return b


def read_private_key(file_path="/root/.ssh/id_rsa") -> bytes:
    with open(file_path, "rb") as x:
        b = x.read()
        return b

# ------------------------公钥加密------------------------
def public_encryption(text: str, public_key: bytes):
    # 字符串指定编码（转为bytes）
    text = text.encode('utf-8')
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(OldRSA.importKey(public_key))
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64

# ------------------------私钥解密------------------------
def private_decryption(text_encrypted_base64: str, private_key: bytes):
    # 字符串指定编码（转为bytes）
    text_encrypted_base64 = text_encrypted_base64.encode('utf-8')
    # base64解码
    text_encrypted = base64.b64decode(text_encrypted_base64)
    # 构建私钥对象
    cipher_private = PKCS1_v1_5.new(OldRSA.importKey(private_key))
    # 解密（bytes）
    text_decrypted = cipher_private.decrypt(text_encrypted, Random.new().read)
    # 解码为字符串
    text_decrypted = text_decrypted.decode()
    return text_decrypted


# ------------------------私钥加密------------------------
def private_encryption(text: str, private_key: bytes):
    # 字符串指定编码（转为bytes）
    text = text.encode('utf-8')
    # 构建公钥对象
    cipher_public = PKCS1_v1_5.new(RSA.importKey(private_key))
    # 加密（bytes）
    text_encrypted = cipher_public.encrypt(text)
    # base64编码，并转为字符串
    text_encrypted_base64 = base64.b64encode(text_encrypted).decode()
    return text_encrypted_base64


# ------------------------公钥解密------------------------
def public_decryption(text_encrypted_base64: str, public_key: bytes):
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
    def __init__(self, user_name='default_name'):

        self.user_path = '/root/.cache/baai_modelhub/user'
        self.cache_path = '/root/.cache/baai_modelhub/'
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        self.user_name=user_name

    def save_user_name(self,user_name):
        self.user_name=user_name
        with open(self.user_path, "w") as x:
            x.write(user_name)
            x.write('\n')



    def obtain_and_set_username(self,user_name='default_name'):
        if user_name =='default_name' or len(user_name)==0:
            if os.path.exists(self.user_path):
                with open(self.user_path, "r") as x:
                    user_name=x.read().strip('\n')
                    if len(user_name)>0:
                        self.user_name= user_name
                return self.user_name
        else:
            self.user_name=user_name
            self.save_user_name(self.user_name)
            return self.user_name



    def passwd_login(self,):
        print('Please type your user name of model.baai.ac.cn (type Enter for default):')
        user_name = input().strip('\n')
        print('Please type your passward (type Enter for default):')
        passward =input()
        print('Please type the verification code of FreeOTP (type Enter for default):')
        opt_vericode = input()
        if true:
            with open(user_path, "w") as x:
                x.write(user_name)
                x.write('\n')

        return is_login



