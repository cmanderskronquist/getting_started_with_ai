from TTS_Silero import SileroTTS

# Example usage:
tts = SileroTTS()
tts.speak()
tts.interrogate()

tts.speak(letmefinish=False)
tts.speak(letmefinish=True)
# print(tts.model.speakers)
#mytext = "The quick brown fox jumps over the lazy dog."
#tts.speak(text=mytext)
# tts.speak(mytext, speaker="en_1" , model_variant='v3_en', sample_rate=48000, language='en')
# tts.speak(mytext, speaker="hokuspokus" , model_variant='v3_de', sample_rate=48000, language='de')
# tts.save("output.wav", mytext, speaker="en_0", sample_rate=24000)