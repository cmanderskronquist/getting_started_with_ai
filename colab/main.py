#!/bin/python3

from helloworld import hello
from gtts import gTTS
from IPython.display import Audio, display, HTML

tts = gTTS('The quick brown fox jumps over the lazy dog.', tld='co.uk')
tts.save('uk.mp3')
tts = gTTS('The quick brown fox jumps over the lazy dog.', tld='com')
tts.save('us.mp3')
tts = gTTS('The quick brown fox jumps over the lazy dog.', tld='com.au')
tts.save('au.mp3')
tts = gTTS('The quick brown fox jumps over the lazy dog.', tld='co.in')
tts.save('in.mp3')
tts = gTTS('The quick brown fox jumps over the lazy dog.', tld='se')
tts.save('se.mp3')

display(HTML('<p>UK:</p>'))
display(Audio('uk.mp3', autoplay=True))

display(HTML('<p>US:</p>'))
display(Audio('us.mp3', autoplay=False))
display(HTML('<p>AU:</p>'))
display(Audio('au.mp3', autoplay=False))
display(HTML('<p>IN:</p>'))
display(Audio('in.mp3', autoplay=False))
display(HTML('<p>SE:</p>'))
display(Audio('se.mp3', autoplay=False))