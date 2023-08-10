import tempfile
import torch
import os
import json
import nemo.collections.asr as nemo_asr
from nemo.collections.asr.data.audio_to_text import AudioToCharDataset


def get_modules(asr_model: str):
    """Extract ASR modules

    Args:
        asr_model (str): _description_

    Returns:
        preprocessor: preprocessor for Audio processing
        ctc_decoder: ctc_decoder for form text 
    """
    quartznet = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name=asr_model, map_location='cpu')
    
    preprocessor = quartznet.preprocessor
    ctc_decoder = quartznet.decoding.ctc_decoder_predictions_tensor
    vocabulary = quartznet.decoder.vocabulary
    del quartznet
    
    return preprocessor, ctc_decoder, vocabulary


def create_inputs(wav_path: str, preprocessor, vocabulary):
    """Create inputs for Tritron Inference Server

    Args:
        wav_path (str): path to wav file
        preprocessor : preprocessor for Audio processing
        vocabulary: vocabulary from ASR model

    Returns:
        processed_signal:           | Inputs for 
        processed_signal_len:       |            Triton Inference Server
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, 'manifest.json'), 'w') as fp:
            entry = {'audio_filepath': wav_path, 'duration': 100000, 'text': 'nothing'}
            fp.write(json.dumps(entry) + '\n')
            
        config = {'paths2audio_files': [wav_path], 'batch_size': 1, 'temp_dir': tmpdir}
        temporary_datalayer = setup_transcribe_dataloader(config, vocabulary)
        for test_batch in temporary_datalayer:
            processed_signal, processed_signal_len = preprocessor(
                input_signal=test_batch[0], length=test_batch[1]
            )
        return processed_signal, processed_signal_len


def setup_transcribe_dataloader(cfg, vocabulary):
    """Utils (torch.utils.data.DataLoader) for ASR Model Inference

    Args:
        cfg : pass
        vocabulary : vocabulary from ASR model

    Returns:
        torch.utils.data.DataLoader
    """
    config = {
        'manifest_filepath': os.path.join(cfg['temp_dir'], 'manifest.json'),
        'sample_rate': 16000,
        'labels': vocabulary,
        'batch_size': min(cfg['batch_size'], len(cfg['paths2audio_files'])),
        'trim_silence': True,
        'shuffle': False,
    }
    dataset = AudioToCharDataset(
        manifest_filepath=config['manifest_filepath'],
        labels=config['labels'],
        sample_rate=config['sample_rate'],
        int_values=config.get('int_values', False),
        augmentor=None,
        max_duration=config.get('max_duration', None),
        min_duration=config.get('min_duration', None),
        max_utts=config.get('max_utts', 0),
        blank_index=config.get('blank_index', -1),
        unk_index=config.get('unk_index', -1),
        normalize=config.get('normalize_transcripts', False),
        trim=config.get('trim_silence', True),
        parser=config.get('parser', 'en'),
    )
    return torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=config['batch_size'],
        collate_fn=dataset.collate_fn,
        drop_last=config.get('drop_last', False),
        shuffle=False,
        num_workers=config.get('num_workers', 0),
        pin_memory=config.get('pin_memory', False),
    )