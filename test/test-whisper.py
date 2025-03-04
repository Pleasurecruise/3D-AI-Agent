import whisper
import config

model = whisper.load_model(name="large-v3", download_root=config.whisper_large)
result = model.transcribe(audio="../assets/asr/zh.wav")
print(result["text"])
