import os
import random
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import google.generativeai as genai
from config import apikey
import requests
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='ec84250793e74d3783f19644240d541f')

def configure_ai():
    genai.configure(api_key=apikey)

def get_news(query):
    try:
        if "news" in query.lower():
            top_headlines = newsapi.get_top_headlines(language='en', page_size=5)
            articles = top_headlines['articles']
            news_info = "\n\n".join([f"Title: {article['title']}\n"
                                     f"Description: {article['description']}\n"
                                     f"Source: {article['source']['name']}\n"
                                     f"URL: {article['url']}" for article in articles])

            # Print the news information
            print(news_info)

            return news_info
        else:
            return "Sorry, I can't fetch news on that topic."
    except Exception as e:
        print(e)
        return "Sorry, I couldn't fetch the news at the moment."


import requests


def get_weather(city):
    api_key = '3fbddd25489f52906f5584e88eb07b4b'  # Replace with your OpenWeather API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"

    try:
        response = requests.get(complete_url)
        data = response.json()

        if data['cod'] == 200:  # Check if API call was successful
            main = data['main']
            weather = data['weather'][0]
            temperature = main['temp']
            pressure = main['pressure']
            humidity = main['humidity']
            description = weather['description']
            weather_info = (f"Weather in {city}:\n"
                            f"Temperature: {temperature}°C\n"
                            f"Pressure: {pressure} hPa\n"
                            f"Humidity: {humidity}%\n"
                            f"Description: {description}")
            return weather_info
        else:
            return f"Error fetching weather data: {data['message']}"

    except Exception as e:
        return f"An error occurred: {e}"

def ai(prompt):
    configure_ai()

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro-001",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    prompt,
                ],
            },
        ]
    )

    response = chat_session.send_message(prompt)

    response_text = ""
    if response and response.candidates:
        response_text = "".join(part.text for part in response.candidates[0].content.parts)

    print(response_text)
    text = f"OpenAI response for Prompt: {prompt}\n***********************************\n{response_text}"

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    file_path = os.path.join("Openai", f"prompt-{random.randint(1, 23434355)}.txt")
    with open(file_path, "w") as f:
        f.write(text)

    return response_text

def say(text, print_text=True):
    if print_text:
        print(text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")

            # Replace special characters including '*'
            query = ''.join(e for e in query if e.isalnum() or e == ' ')

            return query.strip()
        except Exception as e:
            say("Some Error Occurred. Sorry from Jarvis")
            return "Some Error Occurred. Sorry from Jarvis"

def tell_me_a_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you get when you cross a snowman and a vampire? Frostbite.",
        "Why did the math book look sad? Because it had too many problems.",
        "Why can't you give Elsa a balloon? Because she will let it go.",
        "Why don't programmers like nature? It has too many bugs.",
        "How does a penguin build its house? Igloos it together!",
        "What do you call fake spaghetti? An impasta!",
        "Why was the bicycle lying down? It was two-tired.",
        "Why don't skeletons fight each other? They don't have the guts.",
        "Why did the computer go to the doctor? Because it had a virus!",
        "Why did the tomato turn red? Because it saw the salad dressing!",
        "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
        "What do you call cheese that isn't yours? Nacho cheese!",
        "Why don't elephants use computers? Because they are afraid of the mouse!",
        "What did the big flower say to the little flower? Hey, bud!",
        "Why did the bicycle fall over? Because it was two-tired!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why did the coffee file a police report? It got mugged!",
        "How does the ocean say hi? It waves!"
    ]
    return random.choice(jokes)

def open_website_or_app(query):
    sites = [
        ["youtube", "https://youtube.com"],
        ["wikipedia", "https://wikipedia.com"],
        ["google", "https://google.com"],
        ["reddit", "https://reddit.com"],
        ["facebook", "https://facebook.com"],
        ["twitter", "https://twitter.com"],
        ["instagram", "https://instagram.com"],
        ["linkedin", "https://linkedin.com"],
        ["stackoverflow", "https://stackoverflow.com"]
    ]
    apps = {
        "paint": os.path.join(os.environ['windir'], 'system32', 'mspaint.exe'),
        "epic games": r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"
    }
    for site in sites:
        if site[0] in query.lower():
            webbrowser.open(site[1])
            return f"Opening {site[0]}..."
    for app, path in apps.items():
        if app in query.lower():
            os.startfile(path)
            return f"Opening {app}..."
    return f"Sorry, I can't open {query}."

def converse():
    say("Hello! How can I assist you today?")
    while True:
        print("Listening for user's response...")
        user_input = takeCommand()
        if user_input.lower() in ["exit", "quit", "goodbye"]:
            say("Goodbye! Have a great day!")
            break
        if user_input.lower().startswith("open "):
            response_text = open_website_or_app(user_input)
            say(response_text)
        elif "the time" in user_input.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strfTime}")
        elif "using artificial intelligence" in user_input.lower():
            response_text = ai(prompt=user_input)
            say(response_text)
        elif "news" in user_input.lower():
            response_text = get_news(user_input)
            say(response_text, print_text=True)  # Print news before speaking
        else:
            if "how are you" in user_input.lower():
                response_text = "I'm doing great, thank you! How can I assist you today?"
            elif "how is your day going" in user_input.lower():
                response_text = "My day is going well, thanks for asking! How about you?"
            elif "who are you" in user_input.lower():
                response_text = "I am Jarvis AI, your virtual assistant."
            elif "what is your name" in user_input.lower():
                response_text = "My name is Jarvis AI."
            elif "where are you from" in user_input.lower():
                response_text = "I exist in the digital world, created by developers."
            elif "what can you do" in user_input.lower():
                response_text = "I can assist you with various tasks, answer questions, open websites, tell you the time, fetch news, and more."
            elif "tell me a joke" in user_input.lower():
                response_text = tell_me_a_joke()
            else:
                response_text = ai(prompt=user_input)
            say(response_text)

if __name__ == '__main__':
    converse()
