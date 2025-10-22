

# x get user input
# x get LLM output/response
#   get voice/sound output from output
#   play sound received
# x go back to 1

import sys, os
from openai import OpenAI
import sounddevice as sd   
import urllib.request


#UNIX use:
#from playsound import playsound

#WINDOWS use:
import winsound

llmModel = "qwen/qwen3-4b-2507"
gradioURL = "https://3fa0b855d26fcc8663.gradio.live/"

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="funfunfun",
)


def getInput():
	return input("What do you want to know? ")


def fixTextForPrint(text):
    return str(text.encode(sys.stdout.encoding, errors='ignore')).replace('\\x92', '\'').replace('\\x97', '-')

def getLLMResponse2(text):
    
    print("Retrieving response to: " + text)
    
    response = client.responses.create(
        model=llmModel,
        instructions="You are a coding assistant that talks like a pirate.",
        input=text,
    )
    
    actualStr = str(fixTextForPrint(response.output_text))
    
    print("Responded with " + actualStr)

    return actualStr

def getLLMResponse(text):
    return "2 + 2 = 4"

def createVoice(inputText):
    
    from gradio_client import Client, handle_file
    from contextlib import redirect_stdout, redirect_stderr

    with open(os.devnull, "w") as f, redirect_stdout(f), redirect_stderr(f):
        client = Client(gradioURL)
        result = client.predict(
                text=inputText,
                audio_prompt_path=handle_file('https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav'),
                exaggeration=0.5,
                temperature=0.7,
                seed_num=0,
                cfgw=0.7,
                min_p=0.08,
                top_p=1,
                repetition_penalty=1.2,
                api_name="/generate_tts"
        )
        localPath = result[0]
        url = gradioURL + 'gradio_api/file=/tmp'
        actualURL = url + localPath[localPath.index("/gradio/"):]

        return actualURL
	
def playMyAudio(file, asyncMode = False):
    """
    Play audio from a given file using sounddevice.
    """
    from scipy.io import wavfile

    # Read the WAV file
    sample_rate, data = wavfile.read(file)

    # Play the audio
    sd.play(data, samplerate=sample_rate)
    if not asyncMode:
        sd.wait()  # Wait until the file is done playing    


def saveDataToFile(url, tempFile):
    urllib.request.urlretrieve(url, tempFile)

def mainLoop():
    while True:
        try:
            userinput = getInput()
            if userinput == "":
                break
            llmResponse = getLLMResponse(userinput)
            voiceURL = createVoice(llmResponse)
            
            if voiceURL != "":
                tempFile = "temp.wav"
                saveDataToFile(voiceURL, tempFile)
                playMyAudio(tempFile)
        except KeyboardInterrupt:
            print("\nExiting interactive chat.")
            break
        except Exception as e:
            print("An error occurred:", e)


mainLoop()