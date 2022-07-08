from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='GLM-large-ch',
                   model_save_path='./checkpoints/opt-30b-en/',
                    file_name=''
                    )
862876363@qq.com
# import requests
# from baai_modelhub.encryption import public_encryption
# import json
# files_request='http://120.131.5.115:8080/api/downloadCodePasswordTest'
# user_name='862876363@qq.com'
# # encode_passwd=public_encryption(user_name,public_key)
#
# input_key={
#     'user_name': user_name,
#     'password': user_name,
#     'vericode': '308652',
#     'token': '',
#     'model_id': '100000',
#     'file_name': ''
# }
#
#
# data=json.dumps(input_key)
# response=requests.post(files_request,data=data)
# print(response.text)

# def passwd_request(user_name,passwd,googel_vericode,model_id,token='',file_name=''):
#     input_key = {
#         'user_name': user_name,
#         'password': passwd,
#         'vericode': googel_vericode,
#         'token': token,
#         'model_id': model_id,
#         'file_name': file_name
#     }
#     data = json.dumps(input_key)
#     login_request= 'http://120.131.5.115:8080/api/downloadCodePasswordTest'
#     response = requests.post(login_request, data=data)
#
#
#     print(response.text)
#
# user_name='862876363@qq.com'
# passwd='862876363@qq.com'
# googel_vericode='755608'
# model_id='100000'
# passwd_request(user_name,passwd,googel_vericode,model_id)


# from baai_modelhub import AutoPull
# auto_pull = AutoPull()
# auto_pull.get_model(model_name='Glm-large-en',
#                    model_save_path='./checkpoints/',
#                     file_name='pytorch_model.bin'
#                     )
#
# import json
# import requests
# from Crypto.Cipher import PKCS1_v1_5
# from Crypto import Random
# import base64
# from Crypto.PublicKey import RSA as OldRSA
# from baai_modelhub.encryption import passwd_request
#
#
# user_name='862876363@qq.com'
# passwd='862876363@qq.com'
# googel_vericode="035305"
# response=passwd_request(user_name,passwd,googel_vericode)
#
#
# print(response.text)

