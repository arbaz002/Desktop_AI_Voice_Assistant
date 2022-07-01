import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import wolframalpha
import os
import bs4
from bs4 import BeautifulSoup
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re
import json
import pyjokes
import screen_brightness_control as sbc

import vosk
import sounddevice as sd
import queue
import sys

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")

opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })


q=queue.Queue()
device_info=sd.query_devices(1,"input")
sample_rate=device_info["default_samplerate"]
model=vosk.Model("model")

app_id="447E9G-EQ85K9HWYL"
client = wolframalpha.Client(app_id)

def sel_dri():
	print("In sel_dri")
	global driver
	driver = webdriver.Chrome(chrome_options=opt,executable_path="chromedriver.exe")
	#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	#driver.implicitly_wait(10)
	driver.maximize_window()
	return driver


def audio_unrecognized():
	print("Sorry, I lost you there")
	print("Could you please say it again?")

def say(text,engine):
	#print(text)
	engine.say(text)
	engine.runAndWait()

def yes_or_no(engine,r,query):
	q=queue.Queue()

	print("Entered")
	flag=None
	say(query,engine)

	text=""
	with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=lambda indata, frames, time, status: callback(indata, frames, time, status,q)):
		rec = vosk.KaldiRecognizer(model, sample_rate)

		while flag is None:
			while text=="":
				data = q.get()
				if rec.AcceptWaveform(data):
					res=rec.Result()
					text=json.loads(res)["text"].lower()

			if "yes" in text or "no" in text:
				flag="y" if "yes" in text else "n"
			else:
				text=""
				print("Could you please say it again!!!")

	print("Returning the flag: ",flag)
	return flag


def callback(indata, frames, time, status,q,in_main_fn=True):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
        
    if in_main_fn:
   		q.put(bytes(indata))


#commands=["youtube","spotify","google","whatsapp","notepad","gmail","outlook","meet","teams","power off","restart","shut down","weather","temperature","joke","volume up","volume down","increase volume","decrease volume","mute","increase brightness","increase the brightness","decrease brightness","decrease the brightness"]+"what,how,when,why,which,who".split(",")+["what,how,when,why,which,who"]






