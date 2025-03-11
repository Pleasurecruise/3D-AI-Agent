import whisper
import config

model = whisper.load_model(name="base", device="cuda", download_root=config.whisper_base)
result = model.transcribe(audio="../assets/asr/zh.wav")
print(result["text"])
