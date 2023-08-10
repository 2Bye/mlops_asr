from fastapi import FastAPI
# from fast_api_module.utils.audio_utils import get_audio
# from fast_api_module.utils.ASR_modules import get_modules, create_inputs
# from fast_api_module.utils.triton_utils import TritonInferenceClient
# from fast_api_module.data_model.data_model import AudioDataModel, Response

from utils.audio_utils import get_audio
from utils.ASR_modules import get_modules, create_inputs
from utils.triton_utils import TritonInferenceClient
from data_model.data_model import AudioDataModel, Response

app = FastAPI()
preprocessor, ctc_decoder, vocabulary = get_modules('QuartzNet15x5Base-En')


@app.post("/transcribe")
# PROPOSAL:
async def transcribe(metadata: AudioDataModel) -> dict:
    """This function recieve transcription from Triton Inference Server

    Args:
        metadata (dict): some inform.

    Returns:
        results (Response): Results
    """

    audio_path = get_audio(metadata.audio)
    processed_signal, processed_signal_len = create_inputs(wav_path = audio_path,
                                                           preprocessor = preprocessor,
                                                           vocabulary = vocabulary)
    transcription = TritonInferenceClient(processed_signal = processed_signal,
                                          processed_signal_len = processed_signal_len,
                                          ctc_decoder = ctc_decoder)


    results = Response(
        event = "Success",
        text = transcription,
        request_id = metadata.request_id
    )
    
    return results.model_dump()