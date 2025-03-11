import os
import sys
import torchaudio
import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cosyvoice'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cosyvoice/third_party/Matcha-TTS'))

from cosyvoice.cli.cosyvoice import CosyVoice2
from cosyvoice.utils.file_utils import load_wav

model_dir = config.CosyVoice2
cosyvoice = CosyVoice2(model_dir, load_jit=False, load_trt=False, fp16=False)

# 零样本推理生成语言
def zero_shot_usage():
    prompt_speech_16k = load_wav('../assets/tts/zero_shot_prompt.wav', 16000)
    for i, j in enumerate(cosyvoice.inference_zero_shot('收到好友从远方寄来的生日礼物，那份意外的惊喜与深深的祝福让我心中充满了甜蜜的快乐，笑容如花儿般绽放。', '希望你以后能够做的比我还好呦。', prompt_speech_16k, stream=False)):
        output_dir = os.path.join(os.getcwd(), '../output', 'tts')
        os.makedirs(output_dir, exist_ok=True)
        torchaudio.save(os.path.join(output_dir, 'zero_shot_{}.wav'.format(i)), j['tts_speech'], cosyvoice.sample_rate)

# 跨语言推理生成语言
def fine_grained_control():
    prompt_speech_16k = load_wav('../assets/tts/zero_shot_prompt.wav', 16000)
    for i, j in enumerate(cosyvoice.inference_cross_lingual('在他讲述那个荒诞故事的过程中，他突然[laughter]停下来，因为他自己也被逗笑了[laughter]。', prompt_speech_16k, stream=False)):
        output_dir = os.path.join(os.getcwd(), '../output', 'tts')
        os.makedirs(output_dir, exist_ok=True)
        torchaudio.save(os.path.join(output_dir, 'fine_grained_control_{}.wav'.format(i)), j['tts_speech'], cosyvoice.sample_rate)

# 语音指导
def instruct_usage():
    prompt_speech_16k = load_wav('../assets/tts/zero_shot_prompt.wav', 16000)
    for i, j in enumerate(cosyvoice.inference_instruct2('收到好友从远方寄来的生日礼物，那份意外的惊喜与深深的��福让我心中充满了甜蜜的快乐，笑容如花儿般绽放。', '用四川话说这句话', prompt_speech_16k, stream=False)):
        output_dir = os.path.join(os.getcwd(), '../output', 'tts')
        os.makedirs(output_dir, exist_ok=True)
        torchaudio.save(os.path.join(output_dir, 'instruct_{}.wav'.format(i)), j['tts_speech'], cosyvoice.sample_rate)

if __name__ == '__main__':
    zero_shot_usage()
    fine_grained_control()
    instruct_usage()