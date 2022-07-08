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
import warnings
from .encryption import read_private_key, read_public_key,create_rsa_pair
from .encryption import BAAIUserClient
from .encryption import public_encryption, private_decryption, private_encryption, public_decryption
logger = logging.getLogger(__name__.split(".")[0])


def download_from_url(url, total_size=0, to_path=None, file_pname=None, chunk_size=1024 * 1024):
    """
    url: file url
    file_pname: file save name
    chunk_size: chunk size
    resume_download: download from last chunk
    """
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

    if os.path.exists(file_path):
        resume_size = os.path.getsize(file_path)
        if resume_size >= total_size:
            return
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


def obtain_file_lists(model_id,
                   file_name='',
                   user_name='default_name',
                   files_request=None):
    try:
        private_key = read_private_key()
        public_key = read_public_key()
        text_encrypted_base64 = private_encryption(user_name, private_key)
        # text_decrypted = public_decryption(text_encrypted_base64, public_key)

    except:
        public_key,private_key=create_rsa_pair(is_save=False)
        text_encrypted_base64 = private_encryption(user_name, private_key)


    input_key={
        "encrypted_text": text_encrypted_base64,
        "user_name": user_name,
        "model_id": model_id,
        "file_name": file_name
    }
    data=json.dumps(input_key)
    response=requests.post(files_request,data=data)

    texts=json.loads(response.text)

    return texts

class AutoPull(object):
    def __init__(self):
        self.files_request = 'http://120.131.5.115:8080/api/downloadFromCode'


    def get_model(self, model_name,
                   model_save_path='./checkpoints/',
                   file_name='',
                   user_name='default_name'):
        download_path = os.path.join(model_save_path, model_name)
        model_id = _get_model_id(model_name)
        user_client = BAAIUserClient()
        user_name = user_client.obtain_and_set_username(user_name=user_name)

        texts=obtain_file_lists(model_id,
                          file_name=file_name,
                          user_name=user_name,
                          files_request=self.files_request)


        if texts['code']!='200':
            warnings.warn("To download this model, users need login permission. "
                          "The RSA public key on model.baai.ac.cn does not match the user name, "
                          "please check the user name and the RSA public key. You can also login with the user name and password "  )

            try:
                response_dict=user_client.passwd_login(model_id=model_id,file_name=file_name)
                file_list=response_dict['file_list']
                print('login success')
            except:
                raise ValueError(
                    'The user name or the password is invalid, please  check the username and the password'
                    ' on model.aai.ac.cn')
        else:
            file_list=texts['file_list']
            print('login success')


        for file in file_list:
            url = json.loads(file)['url']
            size = json.loads(file)['size']
            file_name = json.loads(file)['file_name']
            download_from_url(url,
                              total_size=size,
                              to_path=download_path,
                              file_pname=file_name
                              )





