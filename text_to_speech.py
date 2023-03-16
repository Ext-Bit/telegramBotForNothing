from gtts import gTTS

def text_to_speech(text):
    tts = gTTS(text=text, lang='ru', slow=False)
    tts.save('test_gtts_file.mp3')
