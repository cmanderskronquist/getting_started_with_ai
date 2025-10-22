#
import sounddevice as sd   

def playMyAudio(file):
    """
    Play audio from a given file using sounddevice.
    """
    from scipy.io import wavfile

    # Read the WAV file
    sample_rate, data = wavfile.read(file)

    # Play the audio
    sd.play(data, samplerate=sample_rate)
    sd.wait()  # Wait until the file is done playing    


#playMyAudio("/Users/sv/skill-AI/getting_started_with_ai/TTS/audio.wav")
