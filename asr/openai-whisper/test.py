import whisper

model = whisper.load_model(name="turbo", download_root="./models")
result = model.transcribe(".//data//zh.wav")
print(result["text"])
