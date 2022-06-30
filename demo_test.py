from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='GLM-10B-ch',
                   model_save_path='./checkpoints/',
                   user_name='羽15928936121',
                    file_name=''
                    )
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

