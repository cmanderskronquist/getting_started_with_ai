from TTS_Silero import SileroTTS
from STT_Silero import SileroSTT

# Example usage:
tts = SileroTTS()
tts.speak()
tts.interrogate()
tts.save(filename="output.wav" , text="The quick brown hyena jumps over the big ugly dog.")
stt = SileroSTT()
stt.transcribe("output.wav")


#tts.speak(speaker = "random")
#tts.speak(letmefinish=False)
#tts.speak(letmefinish=True)
#print(tts.model.speakers)
mytext = "The quick yellow fox jumps over the lazy dog."
# tts.speak(text=mytext,  language='de')
# tts.speak(mytext, speaker="en_1" , model_variant='v3_en', sample_rate=48000, language='en')
tts.speak(mytext, speaker="hokuspokus" , model_variant='v3_de', sample_rate=48000, language='de')
# tts.save("output.wav", mytext, speaker="en_0", sample_rate=24000)