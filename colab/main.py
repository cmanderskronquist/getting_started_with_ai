#!/bin/python3

from helloworld import hello
from gtts import gTTS
from IPython.display import Audio

tts = gTTS('The quick brown fox jumps over the lazy dog.', lang='en-uk')
tts.save('uk.mp3')
tts = gTTS('The quick brown fox jumps over the lazy dog.', lang='en-us')
tts.save('us.mp3')
tts = gTTS('The quick brown fox jumps over the lazy dog.', lang='en-au')
tts.save('au.mp3')

display(Audio('uk.mp3', autoplay=True))
display(Audio('us.mp3', autoplay=False))
display(Audio('au.mp3', autoplay=False))