## Location Setup

change the location of the model in `config.py`, pre-download the model which will be used

```
python download.py
```

### ASR Part

We provide three optional ways below to achieve speech recognition.

#### `FunASR`

click [here](https://github.com/modelscope/FunASR/blob/main/runtime/readme_cn.md) to read the README file directly

#### Through Docker to setup FunASR

suggest to download on server

setup docker client on Linux

```bash
sudo docker pull \
  registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
sudo docker run -p 10096:10095 -it --privileged=true \
  -v $PWD/asr/funasr/models:/workspace/models \
  registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
```
setup docker client on Windows

```bash
docker pull registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
docker run -p 10096:10095 -it --privileged=true -v ${PWD}/asr/funasr/models:/workspace/models registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
```
after setup execute in docker to initialize

```bash
cd FunASR/runtime
nohup bash run_server_2pass.sh \
  --download-model-dir /workspace/models \
  --vad-dir damo/speech_fsmn_vad_zh-cn-16k-common-onnx \
  --model-dir damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-onnx  \
  --online-model-dir damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online-onnx  \
  --punc-dir damo/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727-onnx \
  --lm-dir damo/speech_ngram_lm_zh-cn-ai-wesp-fst \
  --itn-dir thuduj12/fst_itn_zh \
  --hotword /workspace/models/hotwords.txt > log.txt 2>&1 &
```
type the command to see the log

```bash
tail -f /workspace/FunASR/runtime/log.txt
```
Example for directly use

```bash
python asr/funasr/samples/python/funasr_wss_client.py --host "127.0.0.1" --port 10096 --mode 2pass
```
#### openai/whisper

repo address

```
https://github.com/openai/whisper
```
Install Whisper

`ffmpeg` is required

```bash
pip install -U openai-whisper
```
Example for directly use

```bash
whisper ./data/zh.wav --language Chinese --model turbo --model_dir ./models
```
#### paddleasr

## TTS

Reference Repository

### 2noise/ChatTTS

repo address

```
https://github.com/2noise/ChatTTS/blob/main/docs/cn/README.md
```
Install ChatTTS

```bash
pip install ChatTTS
```
Download the model

```python
import ChatTTS
chat = ChatTTS.Chat()
chat.load(compile=False)
```
Example for directly use

```bash
python tts/chattts/test.py
```
### PaddlePaddle/PaddleSpeech

See Above

Common Issue

```
https://github.com/PaddlePaddle/PaddleSpeech/issues/3235
https://github.com/PaddlePaddle/PaddleSpeech/pull/3874
https://github.com/PaddlePaddle/PaddleSpeech/issues/1925
```
require paddlenlp==2.5.2
```bash
paddletts tts --input "你好，欢迎使用百度飞桨深度学习框架！" --output output.wav
```
### FunAudioLLM/CosyVoice

Install CosyVoice

```bash
```python
from modelscope import snapshot_download
snapshot_download('iic/CosyVoice2-0.5B', local_dir='pretrained_models/CosyVoice2-0.5B')
```
Example for directly use

```bash
python tts/cosyvoice2/test.py
```
### RVC-Boss/GPT-SoVITS

Example for directly use

output one sentence through the 3-10s audio

under tts/gpt-sovits

```bash
python tts/gpt-sovits/api.py
```

## OCR

Reference Repository

### PaddlePaddle/PaddleOCR

repo address

```
https://github.com/PaddlePaddle/PaddleOCR
```

Install the package

```bash
pip install paddleocr
```
Example for directly use

```bash
python ocr/paddleocr/test.py
```

## RLS

Example for directly use

```bash
python -m scripts.inference --inference_config configs/inference/test.yaml 
```

## SLM

Reference Repository

### karpathy/nanoGPT

train a character-level GPT on the works of Shakespeare

```bash
python slm/nanogpt/data/shakespeare_char/prepare.py
```
```bash
python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0
```
```bash
python sample.py --out_dir=out-shakespeare-char --device=cpu
```

## LLM

Reference Repository

### deepseek

api docs address

```
https://api-docs.deepseek.com/zh-cn/
```

## LVM

Reference Repository

### deepface

repo address

```
https://github.com/serengil/deepface
```

Install the package

```bash
pip install deepface
```

common issue

change the download path of the model

```
https://blog.csdn.net/xiexvying/article/details/124608954
```