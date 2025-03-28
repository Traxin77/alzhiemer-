import json
import speech_recognition as sr
import pyttsx3
from pymongo import MongoClient
from datetime import datetime

# Initialize text-to-speech engine and recognizer
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen from the microphone and convert speech to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    try:
        # Using Google's speech recognition service
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

def ask_question(question):
    """Ask a question using TTS and return the patient's answer."""
    speak(question)
    answer = listen()
    return answer

def store_to_mongodb(data, connection_string, db_name, collection_name):
    try:
        client = MongoClient(connection_string)
        db = client[db_name]
        collection = db[collection_name]
        result = collection.insert_one(data)
        print("Document inserted with id:", result.inserted_id)
    except Exception as e:
        print("Error inserting document into MongoDB:", e)
    finally:
        client.close()

def main():
    # Ask for patient's name
    patient_name = "prixit"
    
    # Capture the current date and time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Welcome message
    speak("Hello.")
    speak("few questions.")
    
    # List of questions to ask
    questions = [
        "How are you feeling today?",
        "Can you tell me about your day?",
        "Do you have any difficulty remembering recent events?"
    ]
    
    responses = {}
    # Ask each question and collect the answer
    for question in questions:
        answer = ask_question(question)
        responses[question] = answer

    speak("Thank you .")
    # Add patient's name and timestamp to the responses
    responses["patient_name"] = patient_name
    responses["timestamp"] = timestamp
    
    # Save responses to a JSON file locally
    json_filename = "responses.json"
    with open(json_filename, "w") as outfile:
        json.dump(responses, outfile, indent=4)
    
    print("\nPatient responses stored in", json_filename)
    print(json.dumps(responses, indent=4))
    
    # MongoDB Cloud connection details (update with your password)
    mongo_connection_string = "mongodb+srv://root:root@cluster0.s42uhev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    database_name = "alzheimer_db"  # change if needed
    collection_name = "responses"   # change if needed
    
    # Insert the responses into MongoDB
    store_to_mongodb(responses, mongo_connection_string, database_name, collection_name)

if __name__ == "__main__":
    main()
