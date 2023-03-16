import speech_recognition as sr
import subprocess
import os


def speech_to_text(file_name: str, file_name_conv: str):
    r = sr.Recognizer()

    subprocess.call(f'.\\transcribe_audio\\ffmpeg -i .\\transcribe_audio\\{file_name} .\\transcribe_audio\\{file_name_conv}')

    sample_audio = sr.AudioFile('.\\transcribe_audio\\'+file_name_conv)
    with sample_audio as audio_file:
        audio = r.record(audio_file)

    try:
        text = r.recognize_google(audio, language='ru-RU')
    except sr.UnknownValueError:
        text = '"Слов не распознано"'

    os.remove('.\\transcribe_audio\\'+file_name)
    os.remove('.\\transcribe_audio\\'+file_name_conv)
    return text