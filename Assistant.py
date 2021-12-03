import pyttsx3  # converts text to speech
import datetime  # required to resolve any query regarding date and time
import speech_recognition as sr  # required to return a string output by taking microphone input from the user
import wikipedia  # required to resolve any query regarding wikipedia
import webbrowser  # required to open the prompted application in web browser
import os.path  # required to fetch the contents from the specified folder/directory
import smtplib  # required to work with queries regarding e-mail
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By   # required for finding location (web scraping)
import os  # required for hiding sensitive information by storing them in windows environment variable
import requests  # used for API
import datetime,time  # used for delaying the closing of browser
from email.message import EmailMessage  # for sending email



engine = pyttsx3.init(
    'sapi5')  # sapi5 is an API and the technology for voice recognition and synthesis provided by Microsoft
voices = engine.getProperty('voices')  # gets you the details of the current voices
engine.setProperty('voice', voices[0].id)  # 0-male voice , 1-female voice


def speak(audio):  # function for assistant to speak
    engine.say(audio)
    engine.runAndWait()  # without this command, the assistant won't be audible to us


def wishme():  # function to wish the user according to the daytime
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning')

    elif hour > 12 and hour < 18:
        speak('Good Afternoon')

    else:
        speak('Good Evening')

    speak('Hello Sir, I am Friday, your Artificial intelligence assistant. Please tell me how may I help you')


def takecommand():  # function to take an audio input from the user
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 2
        audio = r.listen(source)

    try:  # error handling
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')  # using google for voice recognition
        print(f'User said: {query}\n')
        return query

    except Exception as e:
        speak('Say that again please')
        print('Say that again please...')  # 'say that again' will be printed in case of improper voice
        return 'None'





def weatherinfo(location ):                     #function for weather information using API
    user_api = os.environ['current_weather_data_API']
    complete_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid" + user_api

    api_link = requests.get(complete_link)
    api_data = api_link.json()

    print(api_data)

    temp_city = ((api_data['main']['temp']) - 273.15)
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']

    temp = "temperature is " + temp_city +"Degree celcius"
    speak(temp)

def locate (user_location):
    speak("getting your location")
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.google.com/maps/")

    driver.implicitly_wait(5)

    search = driver.find_element(By.NAME, "q")
    search.send_keys(user_location)
    driver.find_element(By.CLASS_NAME, "xoLGzf-BIqFsb-haAclf").click()

    time.sleep(5)
    driver.close()

def sendemail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    speak("Please enter the email address to whom you want to send email")
    USER_EMAIL = input('user email id : ')
    MY_PASS = os.environ['email_password']
    MY_EMAIL = os.environ['emailid']
    speak("start speaking the message that you want me to deliver")
    msg = takecommand()

    server.login(MY_EMAIL, MY_PASS)

    server.sendmail(MY_EMAIL, USER_EMAIL, msg)
    speak("email sent succefully")
    server.quit()


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand().lower()  # converts user asked query into lower case

        # The whole logic for execution of tasks based on user asked query

        if 'wikipedia' in query:
            speak('Searching Wikipedia....')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=5)
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak('opening youtube')
            webbrowser.open('youtube.com')

        elif 'open google' in query:
            speak('opening google')
            webbrowser.open('google.com')


        elif 'time' in query:
            strtime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'Sir the time is {strtime}')


        elif 'open stack overflow' in query:
            webbrowser.open('stackoverflow.com')

        elif 'open free code camp' in query:
            webbrowser.open('freecodecamp.org')

        elif 'pycharm' in query:
            codepath = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2021.1.3\\bin\\pycharm64.exe"
            os.startfile(codepath)

        elif "open code" in query:
            codePath1 = "C:\\Users\\Pranav Sharma\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath1)


        elif 'how are you' in query:
            speak('I am fine, You are very kind to ask.')

        elif 'news' in query:
            news = webbrowser.open("https://news.google.com/topstories?h1=en-IN&ceid=IN:en&hl=en-IN&gl=IN")
            speak('Here are some latest news from google,Happy reading')
            time.sleep(6)

        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            locate(location)


        elif "weather of" in query:
            speak("getting information")
            location = query.replace("weather of", "")
            weatherinfo(location)

        elif "email" in query:
            sendemail()

        elif 'made you' or 'created you' in query:
            speak('I was Built by vishnudeep and pranav')

        elif "good bye" in query or "ok bye" in query or "stop" in query:
            speak('shutting down,Good bye sir')
            print('shutting down,Good bye sir')
            break


