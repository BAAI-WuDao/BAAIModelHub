from baai_modelhub import AutoPull
auto_pull = AutoPull()
auto_pull.get_model(model_name='GLM-10B-ch',
                   model_save_path='./checkpoints/',
                   user_name='羽1592893612',
                    file_name='vocab.txt'
                    )

