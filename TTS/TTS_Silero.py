import torch
import sounddevice as sd
import numpy as np
from typing import Optional

class SileroTTS:
    def __init__(self, model_variant: str = 'v3_en', language: str = "en", speaker: str = "en_1"):
        self.device = torch.device("cpu")  # Silero TTS works on CPU
        self.model_variant = model_variant
        self.language = language
        self.speaker = speaker
        self.model = None
        self.speakers = None
        self.load_model()

    def load_model(self):
        # Load the Silero TTS model with the correct parameters
        self.model, self.speakers = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                   model='silero_tts',
                                                   language=self.language,
                                                   #speaker=self.model_variant
                                                   )
        
        # Print the available speakers for the loaded model
        print(f"Available speakers for language '{self.language}': {self.speakers}")

        # Validate the speaker
        if self.speaker not in self.speakers:
            raise ValueError(f"Speaker '{self.speaker}' is not valid for language '{self.language}'. "
                             f"Available speakers: {self.speakers}")

    def speak(self, text: str):
        if not self.model:
            raise RuntimeError("Model not loaded. Call `load_model` first.")
        
        # Generate audio using the loaded model and specified speaker
        audio = self.model.apply_tts(text=text,
                                     speaker=self.speaker,
                                     sample_rate=48000)
        
        # Convert the audio to a NumPy array and play it directly
        audio = np.array(audio)  # Ensure it's a NumPy array
        sample_rate = 48000  # Silero TTS default sample rate
        sd.play(audio, samplerate=sample_rate)
        sd.wait()  # Wait until the audio playback is finished

# Example usage:
tts = SileroTTS()  # Ensure the speaker matches the language
mytext = "The quick brown fox jumps over the lazy dog."
tts.speak(mytext)