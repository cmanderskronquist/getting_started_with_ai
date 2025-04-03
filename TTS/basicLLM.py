from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from TTS_Silero import SileroTTS

# Load the model and tokenizer
model_name = "microsoft/phi-1_5"  # You can also use "microsoft/phi-1_5" or a smaller variant
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, 
    device_map="auto", )
tts = SileroTTS()  # Ensure the speaker matches the language

device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

print("LLM uses device: "+device)

# Simple chatbot loop
def chat():
    print("Chatbot is ready! Type 'exit' to quit.")
    history = ""

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Append user input to history
        history += f"User: {user_input}\nAssistant:"

        # Tokenize and generate
        inputs = tokenizer(history, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=100, pad_token_id=tokenizer.eos_token_id)

        # Decode response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the assistant's reply
        reply = response[len(history):].strip().split("\n")[0]
        print("Bot:", reply)
        tts.speak(text=reply)


        # Add reply to history
        history += f" {reply}\n"


chat()
