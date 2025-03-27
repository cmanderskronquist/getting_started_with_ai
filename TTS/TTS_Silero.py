import torch
import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Optional

class SileroTTS:
    def __init__(self, model_variant: str = 'v3_en', language: str = "en", speaker: str = "en_1", hardware: str = "cpu"):
        self.device = torch.device(hardware)  # Silero TTS works on CPU
        self.model_variant = model_variant
        self.language = language
        self.speaker = speaker
        self.model = None
        #self.speakers = None
        self.load_model()


    def load_model(self):
        # Load the Silero TTS model with the correct parameters
        self.model, _ = torch.hub.load('snakers4/silero-models',
                                                   'silero_tts',
                                                   language=self.language,
                                                   speaker=self.model_variant, device=self.device)
        
        # Print the available speakers for the loaded model
        # print(f"Available speakers for language '{self.language}': {self.speakers}")

        # Validate the speaker
        #if self.model_variant not in self.speakers:
        #    raise ValueError(f"Model Variant '{self.model_variant}' is not valid for language '{self.language}'. "
        #                     f"Available speakers: {self.speakers}")

    def audio(self, text: str, speaker: str = None, sample_rate: int = 48000):
        if not self.model:
            self.load_model()
            #raise RuntimeError("Model not loaded. Call `load_model` first.")
        if speaker is None:
            speaker = self.speaker
        # Generate audio using the loaded model and specified speaker
        audio = self.model.apply_tts(text=text,
                                     speaker= speaker,
                                     sample_rate=sample_rate)
        
        # Convert the audio to a NumPy array and play it directly
        audio = np.asarray(audio, dtype=np.float32)  # Use np.asarray for better compatibility
        #sample_rate = 48000  # Silero TTS default sample rate
        return audio
        
    def speak(self, text: str, speaker: str = None, sample_rate: int = 48000):
        audio = self.audio(text, speaker, sample_rate)
        sd.play(audio, samplerate=sample_rate)
        sd.wait()  # Wait until the audio playback is finished

    def save(self, filename: str, text: str, speaker: str = None, sample_rate: int = 48000):
        audio = self.audio(text, speaker, sample_rate)
        sf.write(filename, audio, sample_rate)

# Example usage:
tts = SileroTTS()  # Ensure the speaker matches the language
mytext = "The quick brown fox jumps over the lazy dog."
#tts.speak(mytext, speaker="en_0" , sample_rate=24000)
tts.save("output.wav", mytext, speaker="en_0", sample_rate=24000)

# TODO: Add a function to list available speakers for a given language
# TODO (Optional): Add a function to change the language dynamically
# TODO (Optional): Add a function to change the model variant dynamically
# TODO (Optional): Add a function to save the audio to a file
# TODO (Optional): Add a function to adjust the volume of the audio
# TODO (Optional): Add a function to adjust the speaking rate
# TODO (Optional): Add a function to adjust the pitch of the audio
# TODO (Optional): Add a function to adjust the speaking style (e.g., casual, formal)
# TODO (Optional): Add a function to adjust the language accent (e.g., US English, UK English)
# TODO (Optional): Add a function to adjust the audio quality (e.g., low, medium, high)
# TODO (Optional): Add a function to adjust the audio format (e.g., WAV, MP3, OGG)
# TODO (Optional): Add a function to adjust the audio encoding (e.g., PCM, MP3, Vorbis)
# TODO (Optional): Add a function to adjust the audio effects (e.g., reverb, echo, noise reduction)
# TODO (Optional): Add a function to adjust the audio synthesis method (e.g., Tacotron2, FastSpeech)
# TODO use GPU or Metal optionally
# TODO (Optional): Show momery footprint of model