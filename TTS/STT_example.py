import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
from STT_Silero import SileroSTT  # make sure your class is saved as silero_stt.py or update import

# Set audio params
DURATION = 5  # seconds to record
SAMPLE_RATE = 16000  # required by Silero

def record_audio(duration: int = DURATION, sample_rate: int = SAMPLE_RATE) -> str:
    print(f"🎤 Recording {duration} seconds of audio...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    
    # Save to a temp WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        write(tmpfile.name, sample_rate, audio)
        print(f"✅ Saved to temporary file: {tmpfile.name}")
        return tmpfile.name

def main():
    stt = SileroSTT()  # CPU-only version

    wav_path = '/var/folders/zd/fyg3hrz54rd28b5nvkq_xg240000gn/T/tmp6ilbayqn.wav'
    text = stt.transcribe(wav_path)
    
    print("\n📝 Transcribed Text:")
    print(text)

if __name__ == "__main__":
    main()
