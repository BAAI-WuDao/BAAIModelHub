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


def _get_file_path(download_path, file_name, model_id):
    config_path = os.path.join(str(model_id), file_name)

    dic_download = {'path': config_path}
    config_requests = requests.post('https://model.baai.ac.cn/api/download',
                                    json=dic_download)
    config_requests.encoding = "utf-8"
    if json.loads(config_requests.text)['code'] == '40002':
        file_list = json.loads(config_requests.text)['files']
        print('file {} not exist in {}'.format(file_name, file_list))
        return '40002'
    url = json.loads(config_requests.text)['url']
    size = json.loads(config_requests.text)['size']
    download_from_url(url,
                      total_size=size,
                      to_path=download_path,
                      file_pname=file_name
                      )

    return os.path.join(download_path, file_name)


def _get_model_id(model_name):
    return requests.get('https://model.baai.ac.cn/api/searchModleByName', {
        'model_name': model_name
    }).text


class AutoPull(object):
    def __init__(self):
        self.request = 'http://120.131.5.115:8080/api/searchModelFileByName?model_name='

    def pullmodel(self, model_name, model_save_path='./checkpoints/', file_name=None):
        to_path = os.path.join(model_save_path, model_name)
        print(to_path)
        model_id = _get_model_id(model_name)
        file_requests = requests.get(self.request + model_name)
        file_lists = file_requests.text.replace('"', '').strip('[,]').split(',')
        if file_name is None:
            for file in file_lists:
                print(file, 'loading')
                _get_file_path(to_path, file, model_id)
        else:
            if file_name not in file_lists:
                raise ValueError('Model has no this file')
            else:
                _get_file_path(to_path, file_name, model_id)

        print('model downloaded in ', os.getcwd() + to_path[1:])

if __name__=='__main__':
    auto_pull = AutoPull()
    auto_pull.pullmodel(model_name='cogview2-ch',
                       model_save_path='./checkpoints/'
                       )
