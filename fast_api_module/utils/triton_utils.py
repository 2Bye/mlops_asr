import torch
import tritonclient.http as httpclient


def TritonInferenceClient(processed_signal, processed_signal_len, ctc_decoder) -> str:
    """Function for send audio to Triton Inference Server and recieve text from ASR serivce

    Args:
        processed_signal : input__0 (audio)
        processed_signal_len : input__1 (len vocab)
        ctc_decoder : ASR module

    Returns:
        hypotheses: Transcribe text from ASR Service
    """
    client = httpclient.InferenceServerClient(url="0.0.0.0:8000")
        
    inputs = []
    inputs.append(httpclient.InferInput("input__0", processed_signal.shape, "FP32"))
    inputs.append(httpclient.InferInput("input__1", processed_signal_len.shape, "INT64"))

    inputs[0].set_data_from_numpy(processed_signal.numpy(), binary_data=True)
    inputs[1].set_data_from_numpy(processed_signal_len.numpy(), binary_data=True)

    outputs = httpclient.InferRequestedOutput("output__0", binary_data=True)

    results = client.infer(model_name="quartznet", inputs=inputs, outputs=[outputs])
    inference_output = results.as_numpy('output__0')
    inference_output = torch.Tensor(inference_output)
    hypotheses = ctc_decoder(inference_output)[0][0]
    return hypotheses