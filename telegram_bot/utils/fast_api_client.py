import base64
import requests
from fast_api_module.data_model.data_model import AudioDataModel


def get_text(wav_file: str, HOST_ADDRESS) -> str:
    """Function send wav file to FastAPI Service and recieve TEXT Transcript from ASR service

    Args:
        wav_file (str): path to wav file

    Returns:
        text: ASR Transcript
    """

    with open(wav_file, 'rb') as wav:
        wav_byte = wav.read()
    encoded = base64.b64encode(wav_byte)
    wav_byte = encoded.decode('ascii')

    data = AudioDataModel(audio=wav_byte)

    response = requests.post(f'http://{HOST_ADDRESS}:5454/transcribe', json = data.model_dump())
    return response.json()