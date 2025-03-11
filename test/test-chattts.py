import ChatTTS
import torch
import torchaudio
import config

chat = ChatTTS.Chat()
chat.load(compile=False, source='custom', custom_path=config.ChatTTS)

inputs_en = """
chatTTS is a text to speech model designed for dialogue applications.
[uv_break]it supports mixed language input [uv_break]and offers multi speaker
capabilities with precise control over prosodic elements like
[uv_break]laughter[uv_break][laugh], [uv_break]pauses, [uv_break]and intonation.
[uv_break]it delivers natural and expressive speech,[uv_break]so please
[uv_break] use the project responsibly at your own risk.[uv_break]
""".replace('\n', '') # English is still experimental.

params_refine_text = ChatTTS.Chat.RefineTextParams(
    prompt='[oral_2][laugh_0][break_4]',
)

audio_array_en = chat.infer(inputs_en, params_refine_text=params_refine_text)
torchaudio.save("../output/tts/output.wav", torch.from_numpy(audio_array_en[0]).unsqueeze(0), 24000)
