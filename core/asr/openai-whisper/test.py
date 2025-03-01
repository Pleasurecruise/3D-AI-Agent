import whisper

model_dir = "F:/huggingface/openai/whisper-large-v3"
# model_dir = "/root/autodl-tmp/llm-learning/model/openai/whisper-large-v3"

model = whisper.load_model(name="large-v3", download_root=model_dir)
result = model.transcribe(".//data//zh.wav")
print(result["text"])
