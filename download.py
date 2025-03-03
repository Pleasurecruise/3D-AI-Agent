# download the model from modelscope or huggingface
# config the download path in config.json

from modelscope import snapshot_download
from huggingface_hub import AutoModel
from model import modelscope_model_id_list, huggingface_model_id_list

download_dir = 'f:/modelscope'

# download modelscope model
for model_id in modelscope_model_id_list:
    model_dir = snapshot_download(model_id, cache_dir=download_dir)
    print(f'Model {model_id} downloaded to: {model_dir}')

# download huggingface model
for model_id in huggingface_model_id_list:
    model_dir = AutoModel.from_pretrained(model_id, cache_dir=download_dir)
    print(f'Model {model_id} downloaded to: {model_dir}')