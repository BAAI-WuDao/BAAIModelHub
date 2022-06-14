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
auto_pull.pullmodel(model_name='cogview2-ch',
                    model_save_path='./checkpoints/'
                    )
```

Also, if you only need  one file in the model, you can specify the file name, as an example

```python
from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.pullmodel(model_name='GLM-large-ch',
                    model_save_path='./checkpoints/',
                    file_name='vocab.txt'
                    )
```