from functools import lru_cache
import whisper

@lru_cache(maxsize=2)
def get_model(size: str):
    return whisper.load_model(size)

def transcribe(audio_path: str, model_size: str = 'base') -> str:
    if not audio_path:
        raise ValueError('Upload or record audio first.')
    return get_model(model_size).transcribe(audio_path, fp16=False)['text'].strip()
