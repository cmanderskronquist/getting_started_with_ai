import torch
import os
import numpy as np
from typing import Union

class SileroSTT:
    def __init__(self, language: str = 'en'):
        self.device = torch.device('cpu')
        self.sample_rate = 16000
        self.model, self.decoder, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_stt',
            language=language
        )
        self.model.to(self.device)
        self.read_batch, self.split_into_batches, _, self.prepare_model_input = utils


    def transcribe(self, audio: Union[str, torch.Tensor, np.ndarray], audio_type: str = 'file') -> str:
        if audio_type == 'file':
            if not os.path.exists(audio):
                raise FileNotFoundError(f"Audio file not found: {audio}")
            batch = self.split_into_batches([audio], batch_size=1)
            audio_tensor = self.prepare_model_input(self.read_batch(batch[0]), self.device)
        elif audio_type == 'tensor':
            audio_tensor = audio
        elif audio_type == 'numpy':
            audio_tensor = torch.from_numpy(audio).float().to(self.device)
        else:
            raise ValueError(f"Unsupported audio_type: {audio_type}")

        if audio_tensor.dim() == 1:
            audio_tensor = audio_tensor.unsqueeze(0)
        elif audio_tensor.dim() != 2:
            raise ValueError(f"Invalid tensor shape: {audio_tensor.shape}")

        with torch.no_grad():
            output = self.model(audio_tensor.to(self.device))
        return self.decoder(output[0].cpu())

        def __call__(self, audio: Union[str, torch.Tensor, np.ndarray], audio_type: str = 'file') -> str:
            return self.transcribe(audio, audio_type)
