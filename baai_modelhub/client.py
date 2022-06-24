# 
import copy
import fnmatch
import functools
import importlib.util
import io
import json
import os
import re
import shutil
import sys
from functools import partial
import tarfile
import tempfile
import types
from contextlib import ExitStack, contextmanager
from hashlib import sha256
from pathlib import Path
from typing import Any, BinaryIO, ContextManager, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse
from uuid import uuid4
import numpy as np
from packaging import version
from tqdm.auto import tqdm
import requests
import logging
import json
from .encryption import read_private_key, read_public_key
from .encryption import BAAIUserClient
from .encryption import encryption, decryption
logger = logging.getLogger(__name__.split(".")[0])


def download_from_url(url, total_size=0, to_path=None, file_pname=None, chunk_size=1024 * 1024):
    """
    url: file url
    file_pname: file save name
    chunk_size: chunk size
    resume_download: download from last chunk
    """
    # response = requests.get(url, stream=True, verify=True)
    try:
        response = requests.get(url, stream=True, verify=True)
    except Exception:
        raise ValueError('please check the download file names')

    if to_path is None:
        to_path = './checkpoints/'

    if total_size < 1:
        try:
            total_size = int(response.headers['Content-Length'])
        except Exception as e:
            raise ValueError('please check the url')

    if file_pname is None:
        file_path = os.path.join(to_path, url.split('/')[-1])
    else:
        file_path = os.path.join(to_path, file_pname)

    if not os.path.exists(to_path):
        os.makedirs(to_path)
    if os.path.exists(file_path):
        resume_size = os.path.getsize(file_path)
    else:
        resume_size = 0
    headers = {'Range': 'bytes=%d-' % resume_size}
    res = requests.get(url, stream=True, verify=True, headers=headers)
    progress = tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        total=total_size,
        initial=resume_size,
        desc="Downloading",
        disable=bool(logging.getLogger(__name__.split(".")[0]) == logging.NOTSET),
    )
    while 1:
        with open(file_path, "ab") as f:
            for chunk in res.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    progress.update(len(chunk))
                    f.flush()

        resume_size = os.path.getsize(file_path)
        if resume_size >= total_size:
            break
        else:
            headers = {'Range': 'bytes=%d-' % resume_size}
            res = requests.get(url, stream=True, verify=True, headers=headers)


def _get_model_id(model_name):
    return requests.get('https://model.baai.ac.cn/api/searchModleByName', {
        'model_name': model_name
    }).text


class AutoPull(object):
    def __init__(self):
        self.files_request = 'http://120.131.5.115:8080/api/downloadCodeTest'



    def get_model(self, model_name,
                   model_save_path='./checkpoints/',
                   file_name='',
                   user_name='default_name',
                   login=False,):
        download_path = os.path.join(model_save_path, model_name)
        model_id = _get_model_id(model_name)
        user_client = BAAIUserClient(user_name=user_name)
        public_key = read_public_key()
        private_key = read_private_key()
        # public_key, private_key = create_rsa_pair(is_save=False)

        # 加密
        user_name = user_client.obtain_username()
        print(user_name)

        text_encrypted_base64 = encryption(user_name, private_key)
        print('密文：', text_encrypted_base64)
        # 解密
        # text_decrypted = decryption(text_encrypted_base64, public_key)
        # print('明文：', text_decrypted)
        # user_client.passward_login()


        input_key={
            "encrypted_text": text_encrypted_base64,
            "user_name": user_name,
            "model_id": model_id,
            "file_name": ''
        }
        data=json.dumps(input_key)
        response=requests.post(self.files_request,data=data)
        texts=json.loads(response.text)
        if texts['code']=='40005':
            raise ValueError('To download this model, users need login permission. '
                             'The RSA public key on baai.ac.cn does not mathc the user name,'
                             ' please check the user name and the RSA public key')
        elif texts['code']=='40001':
            raise ValueError('To download this model, users need login permission. '
                             'The user name is not found on baai.ac.cn, please check your user name'
                             'or go to baai.ac.cn to register')
        elif texts['code']=='200':
            pass
        else:
            raise ValueError('Unknown errors')


        file_list = texts['file_list']
        if len(file_name)==0:
            for file in file_list:
                url = json.loads(file)['url']
                size = json.loads(file)['size']
                file_name = json.loads(file)['file_name']
                download_from_url(url,
                                  total_size=size,
                                  to_path=download_path,
                                  file_pname=file_name
                                  )


if __name__=='__main__':


    auto_pull = AutoPull()
    auto_pull.get_model(model_name='GLM-10B-ch',
                         model_save_path='./checkpoints/',
                         user_name='羽1592893612',
                       )


