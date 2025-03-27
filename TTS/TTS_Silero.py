import torch
import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Optional

class SileroTTS:
    def __init__(self, model_variant: str = 'v3_en', language: str = "en", speaker: str = "en_1"):
        # Select device in order: GPU, Metal, CPU
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print(f"Using GPU: {torch.cuda.get_device_name()}")
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            device = torch.device("mps")
            print("Using Metal Performance Shaders (MPS)")
        else:
            device = torch.device("cpu")
            print("Using CPU")
        self.device = device
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
                                        speaker=self.model_variant,
                                        device=self.device)
        
        # Print the available speakers for the loaded model
        # print(f"Available speakers for language '{self.language}': {self.speakers}")

        # Validate the speaker
        #if self.model_variant not in self.speakers:
        #    raise ValueError(f"Model Variant '{self.model_variant}' is not valid for language '{self.language}'. "
        #                     f"Available speakers: {self.speakers}")

    def audio(self, text: str, model_variant: str = None, speaker: str = None, sample_rate: int = 48000, language: str = None):
        model_modified = False
        if model_variant is not None and model_variant != self.model_variant:
            self.model_variant = model_variant
            model_modified = True
        if language is not None and language != self.language:
            self.language = language
            model_modified = True
        if not self.model or model_modified:
            self.load_model()
        if speaker is None:
            speaker = self.speaker
        audio = self.model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate)
        audio = np.asarray(audio, dtype=np.float32)
        return audio

    def speak(self, **kwargs):
        audio = self.audio(**kwargs)
        sample_rate = kwargs.get('sample_rate', 48000)
        sd.play(audio, samplerate=sample_rate)
        sd.wait()

    def save(self, **kwargs):
        audio = self.audio(**kwargs)
        sample_rate = kwargs.get('sample_rate', 48000)
        # Assume filename is provided properly
        sf.write(kwargs.get("filename", "output.wav"), audio, sample_rate)

# Example usage:
#tts = SileroTTS()  # Ensure the speaker matches the language
#mytext = "The quick brown fox jumps over the lazy dog."
#tts.speak(text=mytext)
#tts.speak(mytext, speaker="en_1" , model_variant='v3_en', sample_rate=48000, language='en')
#tts.speak(mytext, speaker="hokuspokus" , model_variant='v3_de', sample_rate=48000, language='de')
#tts.save("output.wav", mytext, speaker="en_0", sample_rate=24000)

# TODO: Add a function to list available speakers for a given language
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