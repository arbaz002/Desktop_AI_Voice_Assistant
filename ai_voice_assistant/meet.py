from dependency_assets import *

text_to_num={"first":1,"second":2,"third":3,"fourth":4,"fifth":5}


def operate_google_meet(text,engine,r,driver):
	#global driver
	print("In operate_google_meet fn:\n\n")
	mx_iter=20
	while True:
		try:
			mute_button=driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[10]/div[3]/div[10]/div[2]/div/div[1]/div/div/span/button')
			camera_button=driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[10]/div[3]/div[10]/div[2]/div/div[2]/div/span/button')
			chat_button=driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[10]/div[3]/div[10]/div[2]/div/div[2]/div/span/button')
			break
		except:
			mx_iter-=1

		if mx_iter==0:
			say("Could not join the meet\n\n",engine)
			return
	while True:
		#say("Would you like to click Microphone icon: ",engine)
		flag=yes_or_no(engine,r,"Would you like to click Microphone icon: ")
		print("Command Received Microphone: ",flag)
		if flag=="y":
			mute_button.click()

		#say("Would you like to click Camera icon: ",engine)
		flag=yes_or_no(engine,r,"Would you like to click Camera icon: ")
		print("Command Received Camera: ",flag)
		if flag=="y":
			camera_button.click()

		sleep(5)

		#say("Would you like to Exit the meet: ",engine)
		flag=yes_or_no(engine,r,"Would you like to Exit the meet: ")
		print("Command Received Exit: ",flag)
		if flag=="y":
			driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[10]/div[3]/div[10]/div[2]/div/div[7]/span/button').click()
			try:
				driver.find_element_by_xpath('//*[@id="yDmH0d"]/div[3]/div[2]/div/div[2]/button[1]').click()
			except:
				pass

			break	


	driver.close()
	return

def join_google_meet(text,engine,r,flag,driver):
	q=queue.Queue()
	in_main_fn=True
	#flag=int(input("Would you like to create a new meet or join a meet 1/2: "))
	print("In Join Google Meet Function:\n\n")
	if flag=="y":
		try:
			#driver.implicitly_wait(10)

			elements=driver.find_elements_by_class_name("wKIIs")
			#print(elements)
			ind=-1
			if len(elements)>0:
				say("I was able to find the following meet scheduled: ",engine)

				for i,element in enumerate(elements):
					#attr=driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
					#print(attr)
					details=element.get_attribute("data-aria-label-static").split(".")
					timing,name=details[0].strip(),details[1].strip()
					code=element.get_attribute("data-call-id").strip()

					say(f"Meet: {name} at {timing} with Meet Code: {code}",engine)

				#say("Please say the rank of meet you would like to join. For example first,second and so on.",engine)
				print("AAAAAAAAAA: ")
				ind=None
				hops=0

				with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=lambda indata, frames, time, status: callback(indata, frames, time, status,q,in_main_fn)):
					rec = vosk.KaldiRecognizer(model, sample_rate)

					while ind is None:
						data = q.get()
						if rec.AcceptWaveform(data):
							res=rec.Result()
							text=json.loads(res)["text"].lower()
							print("Command Received: ",text)

							if any(word in text for word in text_to_num):
								for word in text_to_num:
									if word in text_to_num:
										ind=text_to_num[word]-1
										break

				if ind!=-1:
					print("index: ",ind)
					say("Joining The Meet: "+str(ind),engine)
					elements[ind-1].click()
			else:
				say("Could not find any meet scheduled at the moment.",engine)
				return False

		except:
			say("An error was encountered",engine)
			driver.close()
			return False
	else:
		say("Please the 10 digit meet id",engine)
		meet_id=None

		with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=lambda indata, frames, time, status: callback(indata, frames, time, status,q,in_main_fn)):
				rec = vosk.KaldiRecognizer(model, sample_rate)

				while meet_id is None:
					data = q.get()
					if rec.AcceptWaveform(data):
						res=rec.Result()
						text=json.loads(res)["text"].lower()
						if len(text)==10:
							meet_id=text
						else:
							say("This is an invalid meet id",engine)

		if len(meet_id)!=10:
			print("ID incorrect")
		else:
			driver.find_element_by_xpath('//*[@id="i3"]').send_keys(meet_id)
			driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/button/span').click()

		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source)
			while meet_id is None:
				audio=r.listen(source)
				text=r.recognize_google(audio,language = 'en-IN', show_all = True)['alternative'][0]['transcript'].lower()
				if len(text)==10:
					meet_id=text
				else:
					say("This is an invalid meet id",engine)

		#meet_id=input("Please say the digit meet id: ")
		#meet_id="".join(meet_id.split("-"))

		if len(meet_id)!=10:
			print("ID incorrect")
		else:
			driver.find_element_by_xpath('//*[@id="i3"]').send_keys(meet_id)
			driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/button/span').click()

	mx_iter=20
	print("Loading Screen Meet:\n\n")
	while True:
		joinb=None
		try:
			print("In Try Block:")
			camerab=driver.find_element_by_xpath("//div[@data-tooltip=\"Turn off camera (ctrl + e)\"]")
			if camerab.get_attribute("data-is-muted")=="false":
				driver.implicitly_wait(15)
				camerab.click()

			micb=driver.find_element_by_xpath("//div[@data-tooltip=\"Turn off microphone (ctrl + d)\"]")
			if micb.get_attribute("data-is-muted")=="false":
				driver.implicitly_wait(15)
				micb.click()

			joinb=driver.find_element_by_xpath("//*[@id=\"yDmH0d\"]/c-wiz/div/div/div[10]/div[3]/div/div[1]/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/button")
			driver.implicitly_wait(15)
			joinb.click()
			break
			print("Join Button: ",joinb)

		except:
			sleep(5)
			mx_iter-=1

		print(mx_iter)
		if mx_iter==0:
			say("Some error occured, cannot connect at the moment",engine)
			driver.close()
			return False

	#//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]/div[1]
	operate_google_meet(text,engine,r,driver)

	return True


def open_google_meet(text,engine,r):
	print("Opened Google Meet Function!")
	driver=None
	try:
		driver=sel_dri()
		driver.get("https://meet.google.com/")
		#url="https://accounts.google.com/ServiceLogin?ltmpl=meet&continue=https%3A\%2F\%2Fmeet.google.com\%3Fhs%3D193&"
		driver.find_element_by_xpath('//a[@event-action="sign in"]').click()

		driver.find_element_by_id("identifierId").send_keys("test@gmail.com")  #Your email over here
		driver.find_element_by_xpath('//button[@jscontroller="soHxf"]').click()

		driver.implicitly_wait(15)
		driver.find_element_by_name("password").send_keys("123456") #Password
		driver.implicitly_wait(5)
		driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()
	except:
		say("Chrome Driver isn't working at the moment",engine)
		if driver is not None:
			driver.close()
		return

	#say("Would you like to join a meet from scheduled events or using code: ",engine)
	#say("Say yes to for scheduled events and no otherwise: ",engine)

	#sleep(5)
	#say("Closing google meet",engine)
	#driver.close()
	#return 


	flag=yes_or_no(engine,r,"Would you like to join a meet from scheduled events or using code, Say yes for scheduled events and no otherwise")

	flag=join_google_meet(text,engine,r,flag,driver)

	if not flag:
		f=yes_or_no(engine,r,"Would you like to join a new meet using code, say yes or no: ")

	if f=="y":
		flag=join_google_meet(text,engine,r,1,driver)






