## Environment Setup
Run the following command before executing other commands
Don't change the execute path
```bash
git clone https://github.com/Pleasurecruise/3D-AI-Agent
```
### Question



## ASR
Reference Repository
### modelscope/FunASR
repo address
```
https://github.com/modelscope/FunASR/blob/main/runtime/readme_cn.md
```
#### Through Docker to setup FunASR
suggest to download on server
setup docker client on Linux
```bash
sudo docker pull \
  registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
sudo docker run -p 10096:10095 -it --privileged=true \
  -v $PWD/asr/funasr-runtime-resources/models:/workspace/models \
  registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
```
setup docker client on Windows
```bash
docker pull registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
docker run -p 10096:10095 -it --privileged=true -v ${PWD}/asr/funasr-runtime-resources/models:/workspace/models registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.12
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
python asr/funasr-runtime-resources/samples/python/funasr_wss_client.py --host "127.0.0.1" --port 10096 --mode 2pass
```
### PaddlePaddle/PaddleSpeech
repo address
```
https://github.com/PaddlePaddle/PaddleSpeech
```
Install PaddleSpeech
use numpy==1.23.5!
```bash
pip install paddlepaddle==2.4.2
pip install paddletts
```
Example for directly use
```bash
paddletts asr --lang zh --input zh.wav
```
### openai/whisper
repo address
```
https://github.com/openai/whisper
```
Install Whisper
ffmpeg is required
```bash
pip install -U openai-whisper
```
Example for directly use
```bash
whisper ./data/zh.wav --language Chinese --model turbo --model_dir ./models
```
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
python tts/cosyvoice/test.py
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