from dependency_assets import *

def wolframalpha_response(text,engine,r):
	try:
		ans=next(client.query(text).results).text
	except:
		say("Couldn't find an answer to your question",engine)
		return
	say(ans,engine)


def joke(text,engine,r):
	say(pyjokes.get_joke(),engine)
	return

def power_off(text,engine,r):
	# Directly Power off without any confirmation
	# print("Turning off your device. See you later!")
	# os.system("shutdown /s /t 1")
	print("Do you want to turn off your device? This action will close all the existing programs which are open",engine)
	print("Say yes to proceed or no to cancel the operation",engine)

	flag = 1
	while flag:
		if temp!="yes" and temp!="no":
			audio_unrecognized()
		else:
			flag=0
			if temp=="yes":
				print("Turning off your device. See you later!",engine)
				os.system("shutdown /s /t 1")
			else:
				print("Cancelling the operation",engine)

def restart(text,engine,r):
	# Directly Restart without any confirmation
	# print("Hold tight, restarting your device. See you soon!")
	# os.system("shutdown /r /t  1")
	print("Do you want to restart your device? This action will close all the existing programs which are open",engine)
	print("Say yes to proceed or no to cancel the operation",engine)

	flag = 1
	while flag:
		if temp!="yes" and temp!="no":
			audio_unrecognized()
		else:
			flag=0
			if temp=="yes":
				print("Hold tight, restarting your device. See you soon!",engine)
				os.system("shutdown /r /t  1")
			else:
				print("Cancelling the operation")

def weather(text,engine,r):
	apiKey="73bd116f378ab5a0db373abffeb6f408"
	completeURL="https://api.openweathermap.org/data/2.5/weather?q=mumbai&appid="+apiKey
	response= requests.get(completeURL)
	data= response.json()
	print("telling you the current weather report for Mumbai:",engine)
	curr_temp=round(data["main"]["temp"] - 273.15,2)
	max_temp=round(data["main"]["temp_max"] - 273.15,2)
	min_temp=round(data["main"]["temp_min"] - 273.15,2)
	curr_press=round(data["main"]["pressure"])
	curr_hum=round(data["main"]["humidity"])
	say("the current temperature feels like" + str(curr_temp) + "degree celcius",engine)
	say("the maximum recorded temperature today is" + str(max_temp) + "degree celcius",engine)
	say("the minimum recorded temperature today is" + str(min_temp) + "degree celcius",engine)
	say("the current atmospheric pressure is" + str(curr_press) + "pascals",engine)
	say("the current humidity is" + str(curr_hum) + "percent",engine)


def adjust_volume(text,engine,r):
	if "up" in text or "increase" in text:
		pyautogui.press("volumeup")
		print("the volume has been increased",engine)
	elif "down" in text or "decrease" in text:
		pyautogui.press("volumedown")
		print("the volume has been decreased",engine)
	else:
		print("muting your device",engine)
		pyautogui.press("volumemute")


def adjust_brightness(text,engine,r):
	print("In Function brightness")
	if "up" in text or "increase" in text:
		new_bright=sbc.get_brightness()+10
		# print(new_bright)
		if new_bright>100: new_bright=100
		sbc.set_brightness(new_bright)
	elif "down" in text or "decrease" in text:
		new_bright=sbc.get_brightness()-10
		if new_bright<0: new_bright=0
		sbc.set_brightness(new_bright)

	say(f"brightness has been set to {new_bright} percent",engine)




def power_off_thread():
	os.system("shutdown /s /t 1")

	return


def restart_thread():
	os.system("shutdown /r /t  1")

	return



def increase_volume_thread():
	for i in range(5):
			pyautogui.press("volumeup")

	return


def decrease_volume_thread():
	for i in range(5):
			pyautogui.press("volumedown")
	
	return


def increase_brightness_thread():
	try:
		new_bright=sbc.get_brightness()+10
		if new_bright>100: new_bright=100
		sbc.set_brightness(new_bright)
	except:
		pass

	return 

def decrease_brightness_thread():
	try:
		new_bright=sbc.get_brightness()-10
		if new_bright<0: new_bright=0
		sbc.set_brightness(new_bright)
	except:
		pass
		
	return