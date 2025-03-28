import torch
import numpy as np
from typing import Optional


class SileroTTS:
    def __init__(
        self, model_variant: str = "v3_en", language: str = "en", speaker: str = "en_1"
    ):
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
        self.speed = 1.0
        # self.speakers = None
        self.load_model()

    def load_model(self):
        # Load the Silero TTS model with the correct parameters
        self.model, _ = torch.hub.load(
            "snakers4/silero-models",
            "silero_tts",
            language=self.language,
            speaker=self.model_variant,
            device=self.device,
        )

    def audio(
        self,
        text: str = "The quick brown fox jumps over the lazy dog.",
        model_variant: str = None,
        speaker: str = None,
        sample_rate: int = 48000,
        language: str = None,
        speed: float = None,
    ):
        model_modified = False
        if model_variant is not None and model_variant != self.model_variant:
            self.model_variant = model_variant
            model_modified = True
        if language is not None and language != self.language:
            self.language = language
            model_modified = True
        if speed is not None and speed != self.speed:
            print("Speed:", speed)
            self.speed = speed
            text = self.prosody(text, speed)  # Fixed: update local text variable instead of self.text
        if not self.model or model_modified:
            self.load_model()
        if speaker is None:
            speaker = self.speaker
        audio = self.model.apply_tts(
            text=text, speaker=speaker, sample_rate=sample_rate
        )
        audio = np.asarray(audio, dtype=np.float32)
        return audio

    def prosody(self, text, speed: float = 1.0):
        # TODO: This doesn't seem actually do anything.
        print("Prosony:", speed)
        if speed < 0.25:
            prosody = "x-slow"
        elif speed < 0.75:
            prosody = "slow"
        elif speed < 1.25:
            prosody = "medium"
        elif speed < 1.75:
            prosody = "fast"
        else:
            prosody = "x-fast"
        text = '<speak><prosody rate="' + prosody + '">' + text + '</prosody></speak>'
        print("Text:", text)
        return text

    def speak(self, letmefinish: bool = True, **kwargs):
        import sounddevice as sd
        audio = self.audio(**kwargs)
        sample_rate = kwargs.get("sample_rate", 48000)
        sd.play(audio, samplerate=sample_rate)
        if letmefinish:
            sd.wait()

    def save(self, **kwargs):
        import soundfile as sf
        audio = self.audio(**kwargs)
        sample_rate = kwargs.get("sample_rate", 48000)
        # Assume filename is provided properly
        sf.write(kwargs.get("filename", "output.wav"), audio, sample_rate)

    def interrogate(self):
        def format_size(num_bytes):
            for unit in ["B", "KB", "MB", "GB", "TB"]:
                if num_bytes < 1024.0:
                    return f"{num_bytes:.2f} {unit}"
                num_bytes /= 1024.0
        # TODO (Optional): Expand interrogations
        device = self.device
        if device == torch.device("cuda"):
            #TODO (Optional): Test on a cuda device and show memory summary
            #https://pytorch.org/docs/stable/cuda.html
            #torch.cuda.memory_summary(device=device, abbreviated=True)
            pass
        elif device == torch.device("cpu"):
            print("Using CPU, memory footprint not available.")
        elif device == torch.device("mps"):
            print("MPS Interrogation:")
            print("Max memory: " + format_size(torch.mps.recommended_max_memory()))
            #TODO (Optional): This seems to grossly under-report the memory usage
            print("Allocated memory: " + format_size(torch.mps.driver_allocated_memory()))
        else:
            print("Unknown device: ", device)

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