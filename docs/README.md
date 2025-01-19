## Environment Setup
Run the following command before executing other commands
Don't change the execute path
```bash
git clone https://github.com/Pleasurecruise/3D-AI-Agent
```
## ASR
Reference Repository
### modelscope/funasr
docs address
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
python
```bash
cd asr/funasr-runtime-resources/samples/python
```
```bash
python funasr_wss_client.py --host "127.0.0.1" --port 10096 --mode 2pass
```
