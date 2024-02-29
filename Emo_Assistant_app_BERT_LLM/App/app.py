import streamlit as st
import speech_recognition as sr
import pyttsx3
import wikipedia
import time
import webbrowser
from transformers import pipeline
import re
import numpy as np
from datetime import datetime

# Initialize Speech Recognition and Text-to-Speech
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Emotion Analysis Pipeline
emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')

# CSV File Handling
fieldnames = ['Datetime', 'Recognized Text', 'Emotion Label', 'Emotion Score']
csv_file_path = "emotion_data.csv"

st.set_page_config(
    page_title="Emotion Analysis",
    page_icon="😊",
    layout="wide"
)




st.title("Emotion Analysis Voicebot  💕")




def chatbot_response(sentiment):
    if sentiment == "positive":
        positive_suggestions = [
            "Why not celebrate by treating yourself?",
            "Consider spending some time outdoors.",
            "You could explore a new hobby or activity.",
            "Call a friend and share your positive energy."
        ]
        return f"That's wonderful! I'm glad you're feeling positive. Here are some suggestions to make you feel even more positive:\n{np.random.choice(positive_suggestions)}"
    if sentiment == "joy":
        joy_suggestions = [
            "That's fantastic! Enjoy the moment to the fullest!",
            "Consider sharing your happiness with someone close to you.",
            "Why not plan a fun activity to celebrate?"
        ]
        return f"I can sense your joy! Here are some suggestions to keep the positivity flowing:\n{np.random.choice(joy_suggestions)}"
    elif sentiment == "sadness":
        sadness_suggestions = [
            "I'm sorry to hear that. It's okay to feel sad sometimes. Reach out to friends or family for support.",
            "You might find comfort in your favorite music or a good book.",
            "Consider taking a walk to clear your mind and let your feelings out."
        ]
        return f"I'm here for you during this tough time. Here are some suggestions to help you feel better:\n{np.random.choice(sadness_suggestions)}"
    elif sentiment == "anger":
        anger_suggestions = [
            "Take some deep breaths and try to calm down.",
            "You can write down your feelings to vent your anger.",
            "Consider talking to someone you trust about what's bothering you."
        ]
        return f"It sounds like you're feeling angry. Here are some suggestions to manage your anger:\n{np.random.choice(anger_suggestions)}"
    elif sentiment == "fear":
        fear_suggestions = [
            "It's normal to feel fear sometimes. Try to identify the source of your fear.",
            "Consider practicing relaxation techniques to reduce fear and anxiety.",
            "Reach out to a supportive friend or family member to discuss your fears."
        ]
        return f"I sense fear in your voice. Here are some suggestions to address your fears:\n{np.random.choice(fear_suggestions)}"
    elif sentiment == "surprise":
        surprise_suggestions = [
            "Embrace the element of surprise! Life can be full of unexpected joys.",
            "Explore new experiences and opportunities that come your way.",
            "Take a moment to appreciate the beauty of surprise in everyday life."
        ]
        return f"It seems like you're feeling surprised. Here are some suggestions to make the most of it:\n{np.random.choice(surprise_suggestions)}"
    elif sentiment == "happiness":
        happiness_suggestions = [
            "Celebrate your happiness! Do something that brings you joy.",
            "Share your happiness with loved ones and spread positivity.",
            "Consider setting new goals to keep the happiness going."
        ]
        return f"I sense happiness in your voice! Here are some suggestions to keep the happiness flowing:\n{np.random.choice(happiness_suggestions)}"
    elif sentiment == "love":
        love_suggestions = [
            "Love is a beautiful feeling. Cherish it and express your love to those who matter.",
            "Take time to nurture your relationships and create memorable moments.",
            "Consider doing something thoughtful for someone you love."
        ]
        return f"Love is in the air! Here are some suggestions to embrace and share your love:\n{np.random.choice(love_suggestions)}"
    elif sentiment == "relief":
        relief_suggestions = [
            "Relief is a great feeling. Take a moment to relax and breathe easy.",
            "Reflect on what caused your relief and how you can avoid stress in the future.",
            "Consider celebrating your accomplishments that led to this relief."
        ]
        return f"I sense relief in your voice! Here are some suggestions to make the most of it:\n{np.random.choice(relief_suggestions)}"
    elif sentiment == "contentment":
        contentment_suggestions = [
            "Contentment is precious. Focus on gratitude and appreciate what you have.",
            "Take time to relax and enjoy the present moment without worrying about the future.",
            "Consider sharing your contentment with others and spreading positivity."
        ]
        return f"I sense contentment in your voice! Here are some suggestions to maintain your contentment:\n{np.random.choice(contentment_suggestions)}"
    elif sentiment == "amusement":
        amusement_suggestions = [
            "Amusement is a delightful feeling. Embrace laughter and joy.",
            "Watch or do something funny to keep the amusement going.",
            "Share amusing moments with friends and family for a good laugh."
        ]
        return f"I sense amusement in your voice! Here are some suggestions to keep the amusement flowing:\n{np.random.choice(amusement_suggestions)}"
    elif sentiment == "pride":
        pride_suggestions = [
            "Feeling proud is wonderful. Reflect on your achievements and hard work.",
            "Consider setting new goals to achieve even more and build on your success.",
            "Share your pride with loved ones and inspire them to pursue their dreams."
        ]
        return f"I sense pride in your voice! Here are some suggestions to continue feeling proud:\n{np.random.choice(pride_suggestions)}"
    elif sentiment == "excitement":
        excitement_suggestions = [
            "Excitement is contagious. Embrace it and look forward to new experiences.",
            "Consider planning exciting adventures or activities to keep the thrill alive.",
            "Share your excitement with friends and create memorable moments together."
        ]
        return f"I sense excitement in your voice! Here are some suggestions to make the most of it:\n{np.random.choice(excitement_suggestions)}"
    elif sentiment == "peace":
        peace_suggestions = [
            "Peace is a serene feeling. Take time for relaxation and meditation.",
            "Create a peaceful environment at home and in your daily life.",
            "Consider spreading peace through acts of kindness and understanding."
        ]
        return f"I sense peace in your voice! Here are some suggestions to maintain your inner peace:\n{np.random.choice(peace_suggestions)}"
    elif sentiment == "satisfaction":
        satisfaction_suggestions = [
            "Satisfaction is fulfilling. Reflect on your achievements and accomplishments.",
            "Set new goals to continue feeling satisfied with your progress.",
            "Share your satisfaction with others and inspire them to pursue their dreams."
        ]
        return f"I sense satisfaction in your voice! Here are some suggestions to keep the satisfaction going:\n{np.random.choice(satisfaction_suggestions)}"
    elif sentiment == "lonely":
        lonely_suggestions = [
            "I'm here to chat with you if you're feeling lonely.",
            "Consider reaching out to a friend or loved one to connect.",
            "You can find comfort in activities you enjoy, like reading or listening to music."
        ]
        return f"I sense loneliness in your voice. Here are some suggestions:\n{np.random.choice(lonely_suggestions)}"
    elif sentiment == "heartbroken":
        heartbroken_suggestions = [
            "I'm truly sorry to hear that you're heartbroken. It's okay to grieve.",
            "Lean on your support system and talk to someone about your feelings.",
            "Time can heal. Focus on self-care and healing."
        ]
        return f"I sense heartbreak. Here are some suggestions:\n{np.random.choice(heartbroken_suggestions)}"
    else:
        neutral_suggestions = [
            "You could try a new book or movie to lift your spirits.",
            "Engage in a mindfulness exercise to center yourself.",
            "Plan a small outing to break the routine.",
            "Take a moment to reflect on your day and find the positives."
        ]
        return f"Oh I see. Your feelings are quite balanced. Here are some suggestions:\n{np.random.choice(neutral_suggestions)}"

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError as e:
        st.warning(f"Warning: {e}")




def wishme():
    hour = int(time.strftime("%H"))
    if 0 <= hour < 12:
        speak("Good morning , My name is VoiceBot DDN , How Can I Help You")
    elif 12 <= hour < 18:
        speak("Good afternoon , My name is VoiceBot DDN , How Can I Help You")
    else:
        speak("Good evening , My name is VoiceBot DDN , How Can I Help You")

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError as e:
        st.warning(f"Warning: {e}")

def takeCommand():
    st.write("Speak now...")
    with sr.Microphone() as mic:
        audio = r.listen(mic)
    try:
        command = r.recognize_google(audio)
        st.write("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        st.write("Speech recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results from speech recognition service; {e}")
        return None

def searchWikipedia(query):
    try:
        # Get the full Wikipedia page content for the query
        page = wikipedia.page(query)
        
        # Extract and display all sentences from the page
        sentences = page.content.split('. ')
        
        st.write("According to my Knowledge:")
        for sentence in sentences:
            st.write(sentence)
        
        # Speak the result using text-to-speech
        speak("According to my Knowledge")
        speak('. '.join(sentences))
        
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle DisambiguationError, which occurs when there are multiple possible results
        st.warning("There are multiple possible results. Please specify your query.")
        speak("There are multiple possible results. Please specify your query.")
        
    except wikipedia.exceptions.PageError as e:
        # Handle PageError, which occurs when no information is found for the given query
        st.warning("I couldn't find any information about that.")
        speak("I couldn't find any information about that.")

def openWebsite(url):
    webbrowser.open(url)

def analyze_emotion_from_speech():
    while True:
        st.write("Choose an option:")
        unique_key = f"emotion_analysis_option_{time.time()}"
        option = st.radio("Select an option:", ["Analyze voice tone", "Analyze text input", "Exit"], key=unique_key)

        if option == "Exit":
            st.write("Exiting the emotion analysis.")
            break
        elif option == "Analyze voice tone":
            with sr.Microphone() as source:
                st.write("Speak a sentence:")
                audio = r.listen(source)
            try:
                user_input = r.recognize_google(audio)
                st.write("Recognized text:", user_input)
                emotion_labels = emotion(user_input)
                detected_emotion = emotion_labels[0]['label']
                emotion_score = emotion_labels[0]['score']
                current_datetime = datetime.now()
                st.write("Detected Emotion:", detected_emotion)
                st.write("Emotion Score:", emotion_score)
                st.write("Datetime:", current_datetime)
                advice = chatbot_response(detected_emotion)
                st.write(advice)
                speak(advice)

            except sr.UnknownValueError:
                st.write("Speech recognition could not understand audio.")
            except sr.RequestError as e:
                st.write(f"Could not request results from speech recognition service; {0}".format(e))

        elif option == "Analyze text input":
            user_input = st.text_input("Speak or type a command:")
            if st.button("Process Command"):
                command = user_input.lower()
                emotion_labels = emotion(user_input)
                detected_emotion = emotion_labels[0]['label']
                emotion_score = emotion_labels[0]['score']
                current_datetime = datetime.now()
                st.write("Detected Emotion:", detected_emotion)
                st.write("Emotion Score:", emotion_score)
                st.write("Datetime:", current_datetime)
                advice = chatbot_response(detected_emotion)
                st.write(advice)
                speak(advice)


if __name__ == "__main__":
    wishme()
    while True:
        command = takeCommand()
        if command is not None:
            if "exit" in command:
                st.write("Goodbye!")
                break
            elif "about" in command:
                query = re.search('about (.+)', command).group(1)
                searchWikipedia(query)
                
            elif "open website" in command:
                url = re.search('open website (.+)', command).group(1)
                openWebsite(url)
            elif "time" in command:
                current_time = time.strftime("%I:%M %p")
                st.write(f"The current time is {current_time}.")
                speak(f"The current time is {current_time}.")
            elif "emotion" in command:
                analyze_emotion_from_speech()
            else:
                st.write("I'm sorry, I don't know how to do that.")