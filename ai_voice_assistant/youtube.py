from dependency_assets import *

def operate_youtube_video(text,engine,r,driver):
	q=queue.Queue()
	video_frame=None
	hops=0
	while video_frame is None:
		try:
			video_frame=driver.find_element_by_id('movie_player')
		except:
			hops+=1
			if hops>500: break

	if video_frame is None:
		say("Unable to process the request at the moment",engine)
		return

	"""try:
					video_playing=True# if "playing" in video_frame.get_attribute("class") else False
				except e:
					print(e)
					video_playing=False"""
	
	hops=0
	in_main_fn=True
	video_playing=False

	print("Video successfully opened: ",text,video_playing)
	with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=lambda indata, frames, time, status: callback(indata, frames, time, status,q,in_main_fn)):
		rec = vosk.KaldiRecognizer(model, sample_rate)
		while True:
			data = q.get()
			if rec.AcceptWaveform(data):
				res=rec.Result()
				text=json.loads(res)["text"].lower()

				print("Command received: ",text,"Video Playing: ",video_playing)
				if (video_playing and "pause" in text) or (not video_playing and "play" in text):

					video_frame.send_keys(Keys.SPACE)
					video_playing=not video_playing

				if "skip" in text:
					skip_ads_button=pyautogui.locateCenterOnScreen("skip_ads.PNG")
					if skip_ads_button is not None:
						pyautogui.moveTo(skip_ads_button)
						pyautogui.click()

				if "close" in text:
					in_main_fn=False
					say("Thank you for using Youtube, closing the browser",engine)
					in_main_fn=True
					return


def youtube_search(text,engine,r):
	driver=sel_dri()
	say("Opening Youtube",engine)
	temp=text.lower().split()
	idx=temp.index('youtube')
	query=' '.join(temp[idx+1:])
	say("You made a Youtube search for: "+query,engine)
	url="http://www.youtube.com/results?search_query="+query
	driver.get(url)
	new_url=""
	while new_url=="":
		elems = driver.find_elements_by_tag_name('a')
		for elem in elems:
			href = elem.get_attribute('href')
			if href is not None:
				if "watch" in href:
					new_url=href
					break
	driver.get(new_url)
	sleep(10)
	operate_youtube_video(text,engine,r,driver)
	say("Closed youtube",engine)
	driver.close()

	return
