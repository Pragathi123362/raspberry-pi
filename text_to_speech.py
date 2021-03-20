import pyttsx3

engine = pyttsx3.init()
##engine.say('This is a test phrase.')
##engine.runAndWait()
##voices = engine.getProperty('voices')
####
##print(voices)
####for voice in voices:
####   engine.setProperty('voice', voice.id)
####   engine.say('This is a test phrase.')
####engine.runAndWait()
##engine.setProperty('voice', voices[0].id)
##rate = engine.getProperty('rate')
##print(rate)
##engine.setProperty('rate', 150)
##engine.say('This is a test phrase.')
##engine.runAndWait()
##volume = engine.getProperty('volume')
##print(volume)
id="hello geetha"
#engine.setProperty('volume', 2)
engine.say(id)
engine.runAndWait()


#https://pyshark.com/convert-text-to-speech-using-python/
