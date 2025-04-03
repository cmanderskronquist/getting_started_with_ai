import torch
import os
from typing import Optional, Union

class SileroSTT:
    """
    A wrapper class for Silero Speech-to-Text model.
    
    Attributes:
        model: The loaded Silero STT model
        utils: Model utilities for processing audio
        device: The computation device (CPU/GPU)
        sample_rate: Audio sample rate expected by the model
    """
    
    def __init__(self, 
                 model_name: str = 'silero_stt', 
                 language: str = 'en',
                 device: Optional[str] = None):
        """
        Initialize the Silero STT model.
        
        Args:
            model_name: Name of the Silero model to use
            language: Language code ('en', 'de', 'es', etc.)
            device: Computation device ('cpu', 'cuda', or None for auto-detection)
        """
        self.model, self.utils = None, None
        self.device = self._get_device(device)
        self.sample_rate = 16000  # Silero models typically use 16kHz
        
        self._load_model(model_name, language)
        
    def _get_device(self, device: Optional[str]) -> torch.device:
        """Determine the best computation device."""
        if device is None:
            return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        return torch.device(device)
    
    def _load_model(self, model_name: str, language: str):
        """Load the Silero model and utilities."""
        try:
            torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
            self.model, _ = torch.hub.load(
                repo_or_dir='snakers4/silero-models',
                model=model_name,
                language=language,
                verbose=False
            )
            self.model.to(self.device)
            
            # Get model utils (decoder, etc.)
            (_, self.decoder, _, _, _, _, self.utils) = torch.hub.load(
                repo_or_dir='snakers4/silero-models',
                model='silero_stt',
                language=language,
                verbose=False
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load Silero model: {str(e)}")
    
    def transcribe(self, 
                  audio: Union[str, torch.Tensor, 'np.ndarray'],
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
        # Read audio file and prepare it for the model
        read_audio = self.utils.prepare_model_input(file_path)
        audio_tensor = read_audio.to(self.device)
        return self._transcribe_tensor(audio_tensor)
    
    def _transcribe_tensor(self, audio_tensor: torch.Tensor) -> str:
        """Transcribe audio from torch Tensor."""
        if len(audio_tensor.shape) > 1:
            audio_tensor = audio_tensor.squeeze(0)
            
        # Run inference
        with torch.no_grad():
            output = self.model(audio_tensor)
        
        # Decode output
        return self.decoder(output[0].cpu())
    
    def _transcribe_numpy(self, audio_np: 'np.ndarray') -> str:
        """Transcribe audio from numpy array."""
        audio_tensor = torch.from_numpy(audio_np).to(self.device)
        return self._transcribe_tensor(audio_tensor)
    
    def __call__(self, audio: Union[str, torch.Tensor, 'np.ndarray'],
                 audio_type: str = 'file') -> str:
        """Alias for transcribe method."""
        return self.transcribe(audio, audio_type)