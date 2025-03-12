#!/bin/python3

from helloworld import hello
from gtts import gTTS
from IPython.display import Audio
tts = gTTS('Hello, this is a test of text-to-speech.')
tts.save('test.mp3')

#hello()

display(Audio('test.mp3', autoplay=True))