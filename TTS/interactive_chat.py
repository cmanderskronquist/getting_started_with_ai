import os
import tempfile
import time
import queue
import keyboard  # pip install keyboard
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Import your STT and TTS classes
from STT_Simplero import SileroSTT   # Adjust if your file name or class name differs
from TTS_Silero import SileroTTS

# Define sample rates: STT requires 16kHz, while TTS is set to 48kHz here.
STT_SAMPLE_RATE = 16000
TTS_SAMPLE_RATE = 48000

def record_until_space(sample_rate=STT_SAMPLE_RATE, channels=1, dtype='int16'):
    """
    Record audio until the SPACE key is pressed.
    Audio is captured via a callback and stored in a queue.
    Returns the recorded audio as a NumPy array.
    """
    q = queue.Queue()
    recorded_chunks = []

    def callback(indata, frames, time_info, status):
        q.put(indata.copy())

    print("Recording... Press SPACE to stop.")
    stream = sd.InputStream(samplerate=sample_rate, channels=channels, dtype=dtype, callback=callback)
    with stream:
        while True:
            # Check if SPACE is pressed; if so, break out of loop.
            if keyboard.is_pressed("space"):
                print("Space pressed. Stopping recording.")
                break
            time.sleep(0.1)
        # Drain remaining chunks from the queue
        while not q.empty():
            recorded_chunks.append(q.get())

    if recorded_chunks:
        audio = np.concatenate(recorded_chunks, axis=0)
    else:
        audio = np.array([], dtype=dtype)
    return audio

def main():
    # Initialize STT and TTS engines
    stt = SileroSTT()  # Using default language and settings
    tts = SileroTTS()  # Using default settings

    # Initialize the LLM
    model_name = "microsoft/phi-1_5"  # Adjust the model name if desired
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    llm_model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        torch_dtype=torch.float16, 
        device_map="auto"
    )
    device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    print("LLM is using device:", device)

    history = ""
    print("Interactive chat started. Press Ctrl+C to exit.")

    while True:
        try:
            # Record audio until SPACE is pressed
            audio_data = record_until_space()
            if audio_data.size == 0:
                print("No audio recorded. Please try again.")
                continue

            # Create a temporary WAV file to store the recording
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                temp_filename = tmp_file.name
                write(temp_filename, STT_SAMPLE_RATE, audio_data)
                print(f"Temporary audio saved: {temp_filename}")

            # Transcribe the temporary audio file using the STT flow
            print("Transcribing audio...")
            text = stt.transcribe(temp_filename, audio_type='file')
            print("You said:", text)

            # Delete the temporary file after transcription
            try:
                os.remove(temp_filename)
                print(f"Deleted temporary file: {temp_filename}")
            except Exception as e:
                print("Warning: could not delete temporary file:", e)

            if text.strip() == "":
                print("Could not transcribe any speech. Please try again.")
                continue

            # Update conversation history and call the LLM
            history += f"User: {text}\nAssistant:"
            inputs = tokenizer(history, return_tensors="pt").to(device)
            outputs = llm_model.generate(
                **inputs, 
                max_new_tokens=100, 
                pad_token_id=tokenizer.eos_token_id
            )
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the assistant's reply
            reply = response[len(history):].strip().split("\n")[0]
            print("Bot:", reply)

            # Use TTS to speak out the assistant's reply
            tts.speak(text=reply, sample_rate=TTS_SAMPLE_RATE)
            history += f" {reply}\n"

        except KeyboardInterrupt:
            print("\nExiting interactive chat.")
            break
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()
