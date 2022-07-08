import base64
import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from . import RSA
from Crypto.PublicKey import RSA as OldRSA
import requests
import json

import maskpass



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


def passwd_request(user_name,passwd,googel_vericode,model_id,token='',file_name=''):
    input_key = {
        'user_name': user_name,
        'password': passwd,
        'vericode': googel_vericode,
        'token': token,
        'model_id': model_id,
        'file_name': file_name
    }
    data = json.dumps(input_key)
    login_request= 'http://120.131.5.115:8080/api/downloadCodePasswordTest'

    response = requests.post(login_request, data=data)


    # public_key=b'-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAPtnfRsERmEVoCThY3YD67QYQ+K8hZAQ3wxEnraPSzUKH7n42oBtIGoorx2NsdN6oA9KirGPJjdjvB7Kuszmb90CAwEAAQ==\n-----END PUBLIC KEY-----\n'
    # url="https://usercenter.platform.baai.ac.cn/api/v1/user/login"
    # encode_passwd=public_encryption(passwd,public_key)
    # input_key = {
    #     "ua":"mode",
    #     "logintypes":2,
    #     "username": user_name,
    #     "password": encode_passwd,
    #     "vericode":googel_vericode,
    #     "platformtype": 2
    # }
    # data = json.dumps(input_key)
    # response = requests.post(url, data=data,headers = {'Content-Type': 'application/json' })
    return response

class BAAIUserClient():
    def __init__(self, user_name='default_name'):

        self.user_path = '/tmp/.cache/baai_modelhub/user'
        self.cache_path = '/tmp/.cache/baai_modelhub/'
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        self.user_name=user_name

    def save_user_name(self,user_name):
        self.user_name=user_name
        with open(self.user_path, "w") as x:
            x.write(user_name)
            x.write('\n')

    def obtain_token(self,):
        try:
            with open(os.path.join(self.cache_path,'token_info'),'r') as r:
                token=r.read().strip('\n')
            return token
        except:
            return ''


    def obtain_and_set_username(self,user_name='default_name'):
        if user_name =='default_name' or len(user_name)==0:
            if os.path.exists(self.user_path):
                with open(self.user_path, "r") as x:
                    user_name=x.read().strip('\n')
                    if len(user_name)>0 and user_name is not None:
                        self.user_name= user_name
                return self.user_name
        else:
            self.user_name=user_name
            self.save_user_name(self.user_name)
            return self.user_name
        return self.user_name



    def passwd_login(self,model_id,file_name):

        token=self.obtain_token()
        login = 'fail'
        if len(token)>0:
            try:
                response = passwd_request(self.user_name,
                                          self.user_name,
                                          '888',
                                          model_id=model_id,
                                          token=token,
                                          file_name=file_name)

                response_dict = json.loads(json.loads(response.text))
                if response_dict['code']=='200':
                    login='success'
            except:
                pass
        if login =='fail':
            print('Please type your user name of model.baai.ac.cn:')
            user_name = input()
            password = maskpass.askpass('passward:')
            google_vericode =maskpass.askpass('Verification code from google authenticator:')
            response = passwd_request(user_name,
                                      password,
                                      google_vericode,
                                      model_id=model_id,
                                      file_name=file_name)

            response_dict=json.loads(json.loads(response.text))
            if response_dict['code'] == '200' and len(response_dict['token'])>10:
                login = 'success'
                with open(os.path.join(self.cache_path, 'token_info'), 'w') as w:
                    w.write(response_dict['token'])
                    w.write('\n')
        return response_dict



