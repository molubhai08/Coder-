import requests
import json
import speech_recognition as sr
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='en')

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}



def generate_response(prompt):

    data = {
        "model": "codeguru",
        "prompt": prompt,
        "stream": False
    }

    # Send the request
    response = requests.post(url, headers=headers, data=json.dumps(data))  # Fixed json.dumps
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()  # Directly use .json() to parse JSON
        actual_response = data.get('response')
        return actual_response
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Initialize speech recognition
r = sr.Recognizer()

def record_text():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening...")
            audio2 = r.listen(source2)
            Mytext = r.recognize_google(audio2)
            print(f"Recognized text: {Mytext}")
            return Mytext
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return None


while True:
    text = record_text()
    if text:
        if text.lower() == 'stop':  # Check for stop command before proceeding
            print("Stopping as 'stop' command was received.")
            break
        
        # Translate the spoken text to English
        try:
            translated_text = translator.translate(text)
            print(f"Translated text: {translated_text}")
        except Exception as e:
            print(f"Error in translation: {e}")
            continue

        # Tokenize the translated input and create attention mask
        response = generate_response(translated_text)

        # Generate code from the prompt
        if response:
            print(response)