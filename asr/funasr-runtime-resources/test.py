from funasr import AutoModel
model = AutoModel(model="paraformer-zh",  vad_model="fsmn-vad", punc_model="ct-punc" )
res = model.generate(input="./samples/audio/test.mp4",
            batch_size_s=300)
print(res)