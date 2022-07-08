from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='GLM-large-ch',
                   model_save_path='./checkpoints/opt-30b-en/',
                    file_name=''
                    )
 

