import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import sys
import os

# Initialize speech recognition and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# Set volume to maximum (1.0)
engine.setProperty('volume', 1.0)


def talk(text):
    print(f"Alexa: {text}")  # Print what the assistant is saying
    engine.say(text)
    engine.runAndWait()


def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('Listening...')
            # Adjust for ambient noise
            listener.adjust_for_ambient_noise(source, duration=1)
            # Increase timeout to give more time to speak
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"You said: {command}")
            
            # Check if the command contains "stop" immediately
            if 'alexa stop' in command or 'alexa exit' in command or 'alexa quit' in command:
                talk('Goodbye!')
                sys.exit(0)
                
            # Make the assistant respond to 'alexa' as the wake word
            if 'alexa' in command:
                command = command.replace('alexa', '')
            # Even if no wake word, process the command for testing
    except sr.RequestError:
        print("Could not request results; check your network connection")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except Exception as e:
        print(f"Error: {e}")
    return command


def play_youtube_song(song_name):
    """Function to play a specific song on YouTube"""
    try:
        talk(f'Playing {song_name} on YouTube')
        # Using pywhatkit to search for the song on YouTube
        search_query = song_name.replace(' ', '+')
        # Directly open YouTube with the search query for better accuracy
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        
        # As a backup, also try pywhatkit
        try:
            pywhatkit.playonyt(song_name)
        except:
            pass
            
        return True
    except Exception as e:
        print(f"Error playing YouTube song: {e}")
        talk("I'm having trouble playing that song. Please try again.")
        return False


def run_alexa():
    command = take_command()
    
    if not command:  # If command is empty, ask to repeat
        talk("I didn't catch that. Could you please repeat?")
        return
        
    if 'play' in command:
        song = command.replace('play', '').strip()
        play_youtube_song(song)
    elif 'open youtube' in command:
        talk('Opening YouTube')
        webbrowser.open("https://www.youtube.com")
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who' in command:
        person = command.replace('who', '').replace('is', '').strip()
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except:
            talk("Sorry, I couldn't find information about that person")
    elif 'date' in command:
        talk('Sorry, I have a headache')
    elif 'single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'hello' in command or 'hi' in command:
        talk('Hello there! How can I help you today?')
    elif 'stop' in command or 'exit' in command or 'quit' in command:
        talk('Goodbye!')
        sys.exit(0)
    else:
        talk("I heard you say: " + command)
        talk('Please give me a command I understand.')


# Test the text-to-speech at startup
talk("Hi ! I'm Alexa . What would you like me to do?")

# Main loop
while True:
    try:
        run_alexa()
    except KeyboardInterrupt:
        talk("Shutting down. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error in main loop: {e}")
