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
import pandas as pd
import csv
import plotly.express  as px
import matplotlib.pyplot as plt

r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')


st.set_page_config(
    page_title="Emotion Analysis",
    page_icon="😊",
    layout="wide"
)


st.title("Emotion Analysis Voicebot  💕")

suggestions_df = pd.read_excel("C:\\Users\\svani\\EmoRanda\\Sentiment.xlsx")


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

def chatbot_response(sentiment):
    suggestions = suggestions_df[suggestions_df['Sentiment'].str.lower() == sentiment.lower()]['Suggestions'].tolist()

    if not suggestions:
        return "I'm sorry, I don't have specific suggestions for this sentiment."

    return f"Oh I see, Here are some suggestions to make you feel even better:\n{np.random.choice(suggestions)}"
detected_emotions_list = []

def process_input(user_input):
    emotion_labels = emotion(user_input)
    detected_emotion = emotion_labels[0]['label']
    detected_emotions_list.append(detected_emotion)
    emotion_score = emotion_labels[0]['score']
    current_datetime = datetime.now()
    st.write("Detected Emotion:", detected_emotion)
    st.write("Emotion Score:", emotion_score)
    st.write("Datetime:", current_datetime)
    advice = chatbot_response(detected_emotion)
    st.write(advice)
    speak(advice)

    output_data = {
        'Sentence': [user_input],
        'Detected_Emotion': [detected_emotion],
        'Emotion_Score': [emotion_score],
        'Datetime': [current_datetime],
        'Chatbot_Response': [advice]
    }

    with open("C:\\Users\\svani\\EmoRanda\\Sentiment_Analysis_main.csv", 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  
            writer.writerow(output_data.keys())
        writer.writerow(output_data.values())

def searchWikipedia(query):
    try:
        page = wikipedia.page(query)
        sentences = page.content.split('. ')

        st.write("According to my Knowledge:")
        for i, sentence in enumerate(sentences[:6]):
            st.write(sentence)

        speak("According to my Knowledge")
        speak('. '.join(sentences[:6]))

    except wikipedia.exceptions.DisambiguationError as e:
        st.warning("There are multiple possible results. Please specify your query.")
        speak("There are multiple possible results. Please specify your query.")

    except wikipedia.exceptions.PageError as e:
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
def main():
    wishme()
    st.sidebar.header("User Input")
    input_type = st.sidebar.radio("Select input type:", ["Voice"])

    if input_type == "Voice":
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
                    process_input(command)

    elif input_type == "Text":
        st.sidebar.header("Text Input")
        user_input = st.sidebar.text_input("Type your command:")

        if st.sidebar.button("Process Text Input"):
            process_input(user_input)

def plot_emotions():
    st.header("Detected Emotions Distribution")

    if detected_emotions_list:
        emotion_counts = pd.Series(detected_emotions_list).value_counts().reset_index()
        emotion_counts.columns = ['Emotion', 'Count']

        fig_bar = px.bar(emotion_counts, x='Emotion', y='Count', labels={'Emotion': 'Detected Emotions', 'Count': 'Count'})
        st.plotly_chart(fig_bar)
        fig_pie = px.pie(emotion_counts, values='Count', names='Emotion', title='Detected Emotions Distribution')
        st.plotly_chart(fig_pie)
    else:
        st.info("No emotions detected yet.")
        
if __name__ == "_main_":
    main()
    plot_emotions()