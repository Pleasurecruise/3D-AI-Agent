from funasr import AutoModel

model_dir = "F:/modelscope/iic/SenseVoiceSmall"
# model_dir = "/root/autodl-tmp/llm-learning/model/iic/SenseVoiceSmall"
# model_dir = "F:/modelscope/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
# model_dir = "/root/autodl-tmp/llm-learning/model/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch"

vad_model_dir = "F:/modelscope/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"
# vad_model_dir = "/root/autodl-tmp/llm-learning/model/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"

punc_model_dir = "F:/modelscope/iic/punc_ct-transformer_cn-en-common-vocab471067-large"
# punc_model_dir = "/root/autodl-tmp/llm-learning/model/iic/punc_ct-transformer_cn-en-common-vocab471067-large"

model = AutoModel(
    model=model_dir,
    vad_model=vad_model_dir,
    punc_model=punc_model_dir)

res = model.generate(input="./samples/audio/test.mp4",
            batch_size_s=300)
print(res)