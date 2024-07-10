import os
import time
import uuid
import pyaudio
import playsound
from gtts import gTTS
import openai
import speech_recognition as sr

api_key = "Get ur own openai key!!"
openai.api_key = api_key
language = "nl"

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(f"You said: {said}")
            if "Walter" in said:
                new_string = "This is a predefined response."
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": new_string}]
                )
                text = completion.choices[0].message.content
                speech = gTTS(text=text, lang=language, slow=False)
                file_name = f"welcome_{str(uuid.uuid4())}.mp3"
                speech.save(file_name)
                playsound.playsound(file_name, block=False)
                time.sleep(5)
                os.remove(file_name)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return said

while True:
    get_audio()