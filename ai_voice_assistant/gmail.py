from dependency_assets import *

def compose_email(driver,engine,r):
	q=queue.Queue()
	recipient_box=driver.find_element_by_name("to")
	subject_box=driver.find_element_by_name("subjectbox")
	message_box=driver.find_element_by_css_selector("div[aria-label='Message Body']")

	recipient,subject="arbazahmed.addewala@spit.ac.in",""
	recipient_box.send_keys(recipient)
	say("What should be the subject of the email: ",engine)

	in_main_fn=True
	with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=lambda indata, frames, time, status: callback(indata, frames, time, status,q,in_main_fn)):
		rec = vosk.KaldiRecognizer(model, sample_rate)

		while subject=="":
			data = q.get()
			if rec.AcceptWaveform(data):
				res=rec.Result()
				print(res)
				subject=json.loads(res)["text"].lower()

		subject_box.send_keys(subject)

		in_main_fn=False
		say("What should be the content of the email: ",engine)
		in_main_fn=True
		message,new_sent="",""

		while True:
			new_sent=""
			
			in_main_fn=False
			say("Say the next line: ",engine)
			in_main_fn=True
			while new_sent=="":
				data = q.get()
				if rec.AcceptWaveform(data):
					res=rec.Result()
					print(res)
					new_sent=json.loads(res)["text"].lower()

			if "send" in new_sent.lower():
				break

			message+=new_sent

			in_main_fn=False
			flag=yes_or_no(engine,r,"Would you like to move to a new line, say yes or no:")
			in_main_fn=True
			if flag=="y":
				in_main_fn=False
				say("Moving to a new line",engine)
				in_main_fn=True
				message+="\n\n"

	message_box.send_keys(message)

	sleep(5)
	sendElem = driver.find_element_by_xpath("//div[text()='Send']")
	sendElem.click()

	say("Your Message has been sent successfully!",engine)
	sleep(5)
	say("Closing the browser now, Thank you for using gmail",engine)
	driver.close()
	return

def use_gmail(text,engine,r):
	driver=sel_dri()
	driver.get("https://www.google.com/intl/en-GB/gmail/about/")

	driver.find_element_by_xpath('/html/body/header/div/div/div/a[2]').click()

	driver.find_element_by_id("identifierId").send_keys("arbazahmed.addewala@spit.ac.in") #Email
	driver.find_element_by_xpath('//button[@jscontroller="soHxf"]').click()

	driver.implicitly_wait(15)
	driver.find_element_by_name("password").send_keys("spit@123") #Password
	driver.implicitly_wait(5)
	driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button').click()


	mx_iter=10
	#driver.implicitly_wait(15)
	#driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div').click()
	#compose_email(driver,engine,r)
	while True:
		try:
			driver.implicitly_wait(15)
			driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div').click()
			compose_email(driver,engine,r)
			break
		except:
			mx_iter-=1

		if mx_iter==0:
			say("Was unable to process your request, Sorry",engine)
			driver.close()
			return