import vosk
import sounddevice as sd
import queue
import pyttsx3
import json

q=queue.Queue()


engine=pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def callback(indata, frames, time, status,q,in_main_fn):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)

    if in_main_fn:
   		q.put(bytes(indata))


#print(sd.query_devices())
device_info=sd.query_devices(1,"input")
sample_rate=device_info["default_samplerate"]

model=vosk.Model("model")
in_main_fn=True
with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=lambda indata, frames, time, status: callback(indata, frames, time, status,q,in_main_fn)):
	rec = vosk.KaldiRecognizer(model, sample_rate)
	while True:
		data = q.get()
		res=None
		if rec.AcceptWaveform(data):
			res=rec.Result()
			print(res)

			if res is not None:
				in_main_fn=False
				engine.say(json.loads(res)["text"].lower())
				engine.runAndWait()
				in_main_fn=True
			print("----------",q.qsize())
