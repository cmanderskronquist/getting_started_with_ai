

# x get user input
# x get LLM output/response
#   get voice/sound output from output
#   play sound received
# x go back to 1

import sys

from openai import OpenAI

llmModel = "qwen/qwen3-4b-2507"

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="funfunfun",
)


def getInput():
	return input("What do you want to know? ")


def fixTextForPrint(text):
    return str(text.encode(sys.stdout.encoding, errors='replace')).replace('\\x92', '\'').replace('\\x97', '-')

def getLLMResponse(text):
    
    print("Retrieving response to: " + text)
    
    response = client.responses.create(
        model=llmModel,
        instructions="You are a coding assistant that talks like a pirate.",
        input=text,
    )
    
    print("Responded with " + fixTextForPrint(response.output_text))

    return response.output_text

def createVoice(text):
	# TODO
    print("Voice not yet implemented!")
    return ""
	
def playSound(data):
    print("playSound not yet implemented!")
    # TODO

def mainLoop():
    while True:
        try:
            userinput = getInput()
            if userinput == "":
                break
            llmResponse = getLLMResponse(userinput)
            voiceData = createVoice(llmResponse)
            playSound(voiceData)
        except KeyboardInterrupt:
            print("\nExiting interactive chat.")
            break
        except Exception as e:
            print("An error occurred:", e)


mainLoop()