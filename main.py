import requests
import speech_recognition as sr
import pyttsx3 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import io
from pydub import AudioSegment
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các origin (domain) truy cập
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

@app.post("/api/v1/bot")
async def handle_endpoint(request: Request):
    converter = pyttsx3.init('dummy')
    converter.setProperty('volume', 0.7) 
    voices = converter.getProperty('voices')
    converter.setProperty('voice', voices[1].id)
    rec = sr.Recognizer()

    bot_message = ""
    files = await request.form()

    if "audio" in files:
        audio_file = files['audio'].file.read()
        
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_file))
        audio_segment.export('output.wav', format='wav')
        with sr.AudioFile('output.wav') as source:
            audio_data = rec.record(source)
            
        try:
            query = rec.recognize_google(audio_data, language="vi-VN,en")

            
            print("You Said : {}".format(query))
            r = requests.post('http://localhost:5005/webhooks/rest/webhook', json={"user": "user","message":query})

            for i in r.json():
                print("RASA Said : {}".format(i['text']))
                bot_message += i['text']

        except Exception as e:
            print(e)
            bot_message = "Error processing your request."
    
    else:
        bot_message = "No audio file received."
    
    return {'sender':"bot",'message': bot_message}

# app.run(host='0.0.0.0', port=5000)
