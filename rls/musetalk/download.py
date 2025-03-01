from huggingface_hub import snapshot_download

model_id="TMElyralab/MuseTalk"

snapshot_download(repo_id=model_id, local_dir="F:/huggingface/TMElyralab/MuseTalk",
                  local_dir_use_symlinks=False, revision="main",
                  endpoint='https://hf-mirror.com',
                  resume_download=True)

model_id="stabilityai/sd-vae-ft-mse"

snapshot_download(repo_id=model_id, local_dir="F:/huggingface/stabilityai/sd-vae-ft-mse",
                  local_dir_use_symlinks=False, revision="main",
                  endpoint='https://hf-mirror.com',
                  resume_download=True)

model_id="yzd-v/DWPose"

snapshot_download(repo_id=model_id, local_dir="F:/huggingface/yzd-v/DWPose",
                  local_dir_use_symlinks=False, revision="main",
                  endpoint='https://hf-mirror.com',
                  resume_download=True)

