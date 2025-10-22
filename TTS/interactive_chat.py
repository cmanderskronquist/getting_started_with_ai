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
    Record audio until the SPACE key is pressed using a simpler approach.
    """
    print("Recording... Press SPACE to stop.")
    
    # Pre-allocate a buffer (30 seconds max)
    buffer_size = int(30 * sample_rate)  # 30 seconds buffer
    audio_buffer = np.zeros((buffer_size,), dtype=dtype)
    
    try:
        # Start recording
        with sd.InputStream(
            samplerate=sample_rate,
            channels=channels,
            dtype=dtype,
            blocksize=1024  # Smaller blocksize
        ) as stream:
            
            # Read data directly without callback
            frame_count = 0
            while True:
                if keyboard.is_pressed("space"):
                    print("Space pressed. Stopping recording.")
                    break
                    
                # Read a small chunk of data
                data, overflowed = stream.read(1024)
                if overflowed:
                    print("Warning: Audio buffer overflowed")
                    
                # Calculate remaining space in buffer
                remaining = buffer_size - frame_count
                if remaining <= 0:
                    print("Maximum recording length reached")
                    break
                    
                # Copy data to buffer
                chunk_size = min(len(data), remaining)
                audio_buffer[frame_count:frame_count + chunk_size] = data.flatten()[:chunk_size]
                frame_count += chunk_size
                
                time.sleep(0.001)  # Small sleep to prevent high CPU usage
        
        # Trim the buffer to actual recorded length
        return audio_buffer[:frame_count]
        
    except Exception as e:
        print(f"Error during recording: {e}")
        return np.array([], dtype=dtype)

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
