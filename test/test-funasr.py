import os
import config
import soundfile
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

def non_streaming_asr():
    model = AutoModel(
        model=config.paraformer_zh,
        vad_model=config.fsmn_vad,
        punc_model=config.ct_punc,
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
        disable_update=True,
    )

    res = model.generate(
        input=f"{model.model_path}/example/asr_example.wav",
        cache={},
        language="auto",
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    print(text)

def streaming_asr():
    chunk_size = [0, 10, 5]  # [0, 10, 5] 600ms, [0, 8, 4] 480ms
    encoder_chunk_look_back = 4  # number of chunks to lookback for encoder self-attention
    decoder_chunk_look_back = 1  # number of encoder chunks to lookback for decoder cross-attention

    model = AutoModel(
        model=config.paraformer_zh_streaming,
        disable_update=True,
    )

    wav_file = os.path.join(model.model_path, "example/asr_example.wav")
    speech, sample_rate = soundfile.read(wav_file)
    chunk_stride = chunk_size[1] * 960  # 600ms

    cache = {}
    total_chunk_num = int(len(speech - 1) / chunk_stride + 1)
    for i in range(total_chunk_num):
        speech_chunk = speech[i * chunk_stride:(i + 1) * chunk_stride]
        is_final = i == total_chunk_num - 1
        res = model.generate(input=speech_chunk, cache=cache, is_final=is_final, chunk_size=chunk_size, encoder_chunk_look_back=encoder_chunk_look_back, decoder_chunk_look_back=decoder_chunk_look_back)
        print(res)

if __name__ == "__main__":
    streaming_asr()