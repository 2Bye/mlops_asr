import base64
import random
import string
from pydub import AudioSegment, effects


def get_audio(audio_bytes : str) -> str:
    """Save wavfile from TG Bot 

    Args:
        audio_bytes (str): audio bytes

    Returns:
        audio_name: wav path
    """
    audio_name = ''.join(random.choices(string.ascii_lowercase, k=6))
    audio_name = f'fast_api_module/audio/{audio_name}'
    # audio_name = f'audio/{audio_name}'
    audio_name_ogg = audio_name + '.ogg'
    audio_name_wav = audio_name + '.wav'
    decoded = base64.b64decode(audio_bytes)
    with open(audio_name_ogg,'wb') as f:
        f.write(decoded)

    audio = AudioSegment.from_file(audio_name_ogg)
    if audio.frame_rate != 16000:
        audio = audio.set_frame_rate(16000)
    if audio.channels != 1:
        audio = audio.channels(1)
    audio = effects.normalize(audio)
    audio.export(audio_name_wav, format='wav')
    return audio_name_wav
