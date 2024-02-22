from gtts import gTTS
import os
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
# A dictionary containing all the language codes
language_codes = {
    'kannada': 'kn', 'english': 'en', 'hindi': 'hi', 'marathi': 'mr', 'nepali': 'ne'
    # Add more language codes here
}
# Function to capture voice input through microphone
def capture_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception as e:
        print("Please say that again...")
        return None
# Function to ask for source language
def get_source_language():
    print("Please enter your source language:")
    for lang in language_codes:
        print(lang)
    source_lang = input("Source Language: ").lower()
    while source_lang not in language_codes:
        print("Invalid language. Please enter a valid language.")
        source_lang = input("Source Language: ").lower()
    return language_codes[source_lang]
# Function to ask for target language
def get_target_language():
    print("Please enter your target language:")
    for lang in language_codes:
        print(lang)
    target_lang = input("Target Language: ").lower()
    while target_lang not in language_codes:
        print("Invalid language. Please enter a valid language.")
        target_lang = input("Target Language: ").lower()
    return language_codes[target_lang]
# Function to translate text
def translate_text(text, target_lang):
    translator = Translator()
    translation = translator.translate(text, dest=target_lang)
    return translation.text
# Function to generate and play translated audio
def play_translated_audio(text, target_lang):
    speak = gTTS(text=text, lang=target_lang, slow=False)
    # Save the translated voice to a temporary file
    speak.save('translated_audio.mp3')
    # Play the translated voice
    os.system('start translated_audio.mp3')
# Function to process the uploaded audio file
def process_audio_file(file_path, target_lang):
    r = sr.Recognizer()
    # Detect the file format and convert to wav if necessary
    if file_path.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
    elif file_path.lower().endswith('.wav'):
        audio = AudioSegment.from_wav(file_path)
    else:
        print("Unsupported file format. Please use MP3 or WAV.")
        return
    # Convert and export to a compatible format if necessary
    temp_file = "temp_audio.wav"
    audio.export(temp_file, format="wav")
    # Use the converted file for speech recognition
    with sr.AudioFile(temp_file) as source:
        audio_data = r.record(source)
        try:
            recognized_text = r.recognize_google(audio_data)
            translated_text = translate_text(recognized_text, target_lang)
            print("Translated Text:")
            print(translated_text)
            play_translated_audio(translated_text, target_lang)
        except Exception as e:
            print("Could not recognize the audio. Please try again.", e)
# Main function
def main():
    source_lang = get_source_language()
    target_lang = get_target_language()
    print("Do you want to provide input via microphone or upload an audio file?")
    print("1. Microphone")
    print("2. Upload")
    choice = input("Enter your choice: ")
    if choice == '1':
        input_text = capture_voice()
        if input_text:
            translated_text = translate_text(input_text, target_lang)
            print("Translated Text:")
            print(translated_text)
            play_translated_audio(translated_text, target_lang)
    elif choice == '2':
        audio_file_path = input("Please provide the full path to the audio file: ")
        if os.path.exists(audio_file_path):
            process_audio_file(audio_file_path, target_lang)
        else:
            print("File not found. Please provide a valid file path.")
    else:
        print("Invalid choice")
if __name__ == "__main__":
    main()