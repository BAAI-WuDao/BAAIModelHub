# BAAIModelHub

BAAIModelHub is a tool for managing models from [model.baai.ac.cn](https://model.baai.ac.cn/).

## install
one can install BAAIModelHub from pip as

```shell
pip install baai_modelhub
```
 or 

```shell
git clone git@github.com:BAAI-WuDao/BAAIModelHub.git
cd BAAIModelHub
python setup.py install
```

## download models

One can download models from [model.baai.ac.cn](https://model.baai.ac.cn/) with model name as

```python
from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='cogview2-ch',
                    model_save_path='./checkpoints/'
                    )
```

Also, if you only need  one file in the model, you can specify the file name, as an example

```python
from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='GLM-large-ch',
                    model_save_path='./checkpoints/',
                    file_name='vocab.txt'
                    )
```

Some models on [model.baai.ac.cn](https://model.baai.ac.cn/) may need login access

To do this, one need to upload the RSA public key (in the file ```~/.ssh/id_rsa.pub```) to the platform [model.baai.ac.cn](https://model.baai.ac.cn/) and one can login without password.
Also, one can login with the ```user_name```,  ```password``` and ```google authorization``` which would be required if the RSA public key is not uploaded. One can follow the instruction to
upload the public key and obtain the ```google authorization```.

With ```user_name```, one can down model files as 
```python
from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='GLM-large-ch',
                    model_save_path='./checkpoints/',
                    usr_name='****'
                    )
```
or download only one file as 
```python
from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='GLM-large-ch',
                    model_save_path='./checkpoints/',                  
                    file_name='vocab.txt',
                    usr_name_name='****'
                    )
```

