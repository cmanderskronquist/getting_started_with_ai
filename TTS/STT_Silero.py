import torch
import os
import numpy as np
from typing import Optional, Union

class SileroSTT:
    """
    A CPU-only wrapper class for Silero Speech-to-Text model.
    
    Attributes:
        model: The loaded Silero STT model
        decoder: Decoder function for model output
        utils: Utility functions for audio processing
        device: Set to 'cpu' explicitly
        sample_rate: Audio sample rate expected by the model
    """
    
    def __init__(self, language: str = 'en'):
        """
        Initialize the Silero STT model (CPU only).
        
        Args:
            language: Language code ('en', 'de', 'es', etc.)
        """
        self.device = torch.device('cpu')  # Force CPU
        self.sample_rate = 16000  # Silero models typically use 16kHz
        self.model = self._load_model(language)
        
    def _load_model(self, language: str):
        """Load the Silero STT model and utility functions (CPU only)."""
        try:
            torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
            result = torch.hub.load(
                repo_or_dir='snakers4/silero-models',
                model='silero_stt',
                language=language
            )
            
            # Debug: Print the result to understand its structure
            # print(f"Loaded model result: {result}")
            
            # Adjust unpacking based on the actual return structure
            if isinstance(result, tuple) and len(result) == 3:
                model, decoder, utils = result
            else:
                raise ValueError("Unexpected return structure from torch.hub.load")
            
            model.to(self.device)

            # Unpack the tuple of utility functions
            read_batch, _, _, prepare_model_input = utils
            self.read_batch = read_batch
            self.prepare_model_input = prepare_model_input
            self.decoder = decoder  # Use the decoder object directly

            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load Silero model: {str(e)}")

    
    def transcribe(self, 
                   audio: Union[str, torch.Tensor, np.ndarray],
                   audio_type: str = 'file') -> str:
        """
        Transcribe audio to text.
        
        Args:
            audio: Input audio (file path, torch Tensor, or numpy array)
            audio_type: Type of input ('file', 'tensor', or 'numpy')
            
        Returns:
            Transcribed text
        """
        if audio_type == 'file':
            if not os.path.exists(audio):
                raise FileNotFoundError(f"Audio file not found: {audio}")
            return self._transcribe_file(audio)
        elif audio_type == 'tensor':
            return self._transcribe_tensor(audio)
        elif audio_type == 'numpy':
            return self._transcribe_numpy(audio)
        else:
            raise ValueError(f"Unsupported audio_type: {audio_type}. Use 'file', 'tensor', or 'numpy'")
    
    def _transcribe_file(self, file_path: str) -> str:
        """Transcribe audio from file."""
        batch = self.read_batch([file_path])  # Use self.read_batch
        print(f"Debug: Batch content: {batch}")  # Debug: Inspect batch content

        # Ensure batch[0] is at least 2-dimensional (batch size, sequence length)
        if isinstance(batch[0], torch.Tensor):
            if batch[0].dim() == 1:  # If it's 1-dimensional, add a batch dimension
                batch[0] = batch[0].unsqueeze(0)
            elif batch[0].dim() == 0:  # If it's 0-dimensional, raise an error
                raise ValueError("Invalid tensor format: batch[0] is 0-dimensional")

        input_tensor = self.prepare_model_input(batch[0], self.device)  # Use self.prepare_model_input
        return self._transcribe_tensor(input_tensor)
    
    def _transcribe_tensor(self, audio_tensor: torch.Tensor) -> str:
        """Transcribe audio from torch Tensor."""
        # Ensure the tensor is 2-dimensional (batch size, sequence length)
        if audio_tensor.dim() == 1:  # If it's 1-dimensional, add a batch dimension
            audio_tensor = audio_tensor.unsqueeze(0)
        elif audio_tensor.dim() != 2:  # If it's not 2-dimensional, raise an error
            raise ValueError(f"Invalid tensor shape: {audio_tensor.shape}. Expected 2 dimensions.")

        # Run inference
        with torch.no_grad():
            output = self.model(audio_tensor.to(self.device))
            print(f"Debug: Model output shape: {output.shape}")  # Debug: Inspect model output shape
        
        # Decode output using the decoder object
        return self.decoder(output.cpu())
    
    def _transcribe_numpy(self, audio_np: np.ndarray) -> str:
        """Transcribe audio from numpy array."""
        audio_tensor = torch.from_numpy(audio_np).float().to(self.device)
        return self._transcribe_tensor(audio_tensor)
    
    def __call__(self, audio: Union[str, torch.Tensor, np.ndarray],
                 audio_type: str = 'file') -> str:
        """Alias for transcribe method."""
        return self.transcribe(audio, audio_type)
