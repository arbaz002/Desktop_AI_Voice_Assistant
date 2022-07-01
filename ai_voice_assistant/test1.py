from dependency_assets import *


"""with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=callback):
	rec = vosk.KaldiRecognizer(model, sample_rate)
	while True:
		data = q.get()
		if rec.AcceptWaveform(data):
			print(data)
			print(rec.Result())
			break"""

print(sd.query_devices())