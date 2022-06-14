# coghub

BAAIModelHub is a tool for managing models from [model.baai.ac.cn](model.baai.ac.cn).


## download models

The [utils/modelhub/client.py](coghub/client.py) contains the API for downing models and files.
 
One can download models from [model.baai.ac.cn](model.baai.ac.cn) with model name as

```python
from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.pullmodel(model_name='cogview2-ch',
                    model_save_path='./checkpoints/'
                    )
```
