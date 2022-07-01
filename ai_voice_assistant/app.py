from tkinter import *
from PIL import ImageTk,Image
from tkinter import font
from tkinter.filedialog import askopenfile
import time
import threading


from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)



from dependency_assets import *
from youtube import *
from google import *
#from notepad import *
from gmail import *
from system_operations import *
from meet import *

r=sr.Recognizer()
engine=pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('voice', engine.getProperty('voices')[1].id)


#commands=["youtube","spotify","google","whatsapp","notepad","gmail","outlook","meet","teams","power off","restart","shut down","weather","temperature","joke","volume up","volume down","increase volume","decrease volume","mute","increase brightness","increase the brightness","decrease brightness","decrease the brightness"]+"what,how,when,why,which,who".split(",")+["what,how,when,why,which,who"]

COMMANDS={
	"tube,youtube": youtube_search,
	"google": google_search,
	"spotify": None,
	"whatsapp": None,
	"notepad": None,#write_text_in_notepad,
	"email": use_gmail,
	"outlook": None,
	"meet": open_google_meet,
	"teams": None,
	"power off,shut down": power_off,
	"restart": restart,
	"weather,temperature": weather,
	"joke": joke,
	"volume,mute": adjust_volume,
	"brightness": adjust_brightness,
	"what,how,when,why,which,who": wolframalpha_response
}


def verify_file_name(text):
	print(f"is it {text}?",engine)

	with sr.Microphone as source:
		r.adjust_for_ambient_noise(source)
		audio=r.listen(source)

		while True:
			response=r.recognize_google(audio,language = 'en-IN', show_all = True)['alternative'][0]['transcript'].lower()
			if response=="":
				continue

			if "yes" in response:
				return True
			else:
				return False 


def verify_name():
	flag,hops=None,1

	with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=callback):
		rec = vosk.KaldiRecognizer(model, sample_rate)
		while flag is None:
			data = q.get()
			if rec.AcceptWaveform(data):
				flag=rec.Result()["text"].lower()
			elif hops%5==0:
				print("Please confirm it again",engine)
			else:
				hops+=1

	return flag

def get_name():
	print(type(q))
	name=""
	
	with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=callback):
		rec = vosk.KaldiRecognizer(model, sample_rate)

		while name=="":
			data = q.get()
			if rec.AcceptWaveform(data):
				res=rec.Result()
				#print(res)
				name=json.loads(res)["text"].lower()
				print("Name ",name)

	return name




class TkinterApp(Tk):

	def __init__(self):

		Tk.__init__(self)

		self.title("My Personal Voice Assistant")
		self.geometry("1043x611")
		self.container=Frame(self,bg="#ffffff")
		self.container.pack(fill='both',expand=True)
		self.resizable(False,False)
		self.curr=0
		#self.title_icon=ImageTk.PhotoImage(Image.open("icon.png"))
		#self.iconphoto(False,self.title_icon)
	def get_frames(self):
		
		self.frames=[]

		for i in range(2):
			frame=HomePage(self.container,self,i)
			#frame.rowconfigure(0,weight=1)
			#frame.columnconfigure(0,weight=1)
			self.frames.append(frame)
			frame.place(relx=0,rely=0,height=400,width=700)

		self.current_frame=self.frames[0]
		self.current_frame.stop=False
		self.current_frame.display_content()	
		self.current_frame.tkraise()

	def update_frame(self):
		self.curr=(self.curr+1)%2
		self.current_frame=self.frames[self.curr]
		self.current_frame.stop=False
		self.current_frame.display_content()
		self.current_frame.tkraise()
		print(self.current_frame.flag)

		if self.current_frame.flag:
			threading.Thread(target=self.current_frame.speak).start()

				

class HomePage(Frame):

	def __init__(self,master,parent,flag):

		Frame.__init__(self,master,bg="#000000")

		self.parent=parent
		self.master=master
		self.flag=flag
		self.bg=PhotoImage(file=relative_to_assets("image_1.png"))
		self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))

		if not self.flag:
			self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
		else:
			self.button_image_2 = PhotoImage(file=relative_to_assets("button_7.png"))

		self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
		self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
		self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
		self.button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
		self.button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
		#self.icon=ImageTk.PhotoImage(Image.open("icon_1.png"))


	def display_content(self):
		#self.place(relx=0,rely=0,height=400,width=700)
		for widgets in self.winfo_children():
			widgets.destroy()	

		print("2222",self.flag)
		self.canvas = Canvas(
		    bg = "#FFFFFF",
		    height = 611,
		    width = 1043,
		    bd = 0,
		    highlightthickness = 0,
		    relief = "ridge"
		)
		self.canvas.place(x=0,y=0)

		self.canvas.create_image(
		    521.0,
		    305.0,
		    image=self.bg
		)

		
		self.canvas.create_rectangle(
		    0.0,
		    122.0,
		    1043.0,
		    207.0,
		    fill="#E25858",
		    outline="")

		self.canvas.create_text(
		    605.0,
		    215.0,
		    anchor="nw",
		    text="Volume Control",
		    fill="#FFFFFF",
		    font=("FontAwesome5Free Regular", 20 * -1)
		)

		self.canvas.create_text(
		    93.0,
		    155.0,
		    anchor="nw",
		    text="Power Off",
		    fill="#000000",
		    font=("FontAwesome5Free Regular", 20 * -1)
		)

		self.canvas.create_text(
		    251.0,
		    52.0,
		    anchor="nw",
		    text="My Personal Voice Assistant",
		    fill="#FFFFFF",
		    font=("FontAwesome5Free Regular", 40 * -1)
		)

		self.button_1 = Button(
		    image=self.button_image_1,
		    borderwidth=0,
		    highlightthickness=0,
		    command=lambda: print("Restarting the Computer"),#restart_thread#lambda: print("hhhh"),
		    relief="flat"
		)

		self.button_1.place(
		    x=287.0,
		    y=138.0,
		    width=223.0,
		    height=56.0
		)

		self.canvas.create_text(
		    847.0,
		    215.0,
		    anchor="nw",
		    text="Brightness \nControl",
		    fill="#FFFFFF",
		    font=("FontAwesome5Free Regular", 20 * -1)
		)

		self.canvas.create_rectangle(
		    0.0,
		    402.0,
		    1043.0,
		    506.0,
		    fill="#E25959",
		    outline="")

		self.button_2 = Button(
		    image=self.button_image_2,
		    borderwidth=0,
		    highlightthickness=0,
		    command=lambda: self.fn(),
		    relief="flat"
		)
		self.button_2.place(
		    x=384.0,
		    y=419.0,
		    width=275.0,
		    height=70.0
		)

		self.button_3 = Button(
		    image=self.button_image_3,
		    borderwidth=0,
		    highlightthickness=0,
		    command=lambda: print("Powering Off the Computer"),#power_off_thread,#lambda: print("fgfgfg"),
		    relief="flat"
		)
		self.button_3.place(
		    x=34.0,
		    y=138.0,
		    width=217.0,
		    height=56.0
		)


		self.button_4 = Button(
		    image=self.button_image_4,
		    borderwidth=0,
		    highlightthickness=0,
		    command=lambda: threading.Thread(target=decrease_brightness_thread).start(),#lambda: print("button_4 clicked"),
		    relief="flat"
		)
		self.button_4.place(
		    x=906.0,
		    y=135.0,
		    width=58.0,
		    height=59.0
		)

		self.button_5 = Button(
		    image=self.button_image_5,
		    borderwidth=0,
		    highlightthickness=0,
		    command=lambda: threading.Thread(target=increase_brightness_thread).start(),#lambda: print("button_5 clicked"),
		    relief="flat"
		)
		self.button_5.place(
		    x=825.0,
		    y=136.0,
		    width=58.0,
		    height=60.0
		)

		self.button_6 = Button(
		    image=self.button_image_6,
		    borderwidth=0,
		    highlightthickness=0,
		    command=lambda: threading.Thread(target=increase_volume_thread).start(),#lambda: print("button_6 clicked"),
		    relief="flat"
		)
		self.button_6.place(
		    x=605.0,
		    y=136.0,
		    width=58.0,
		    height=60.0
		)

		self.button_7 = Button(
		    image=self.button_image_7,
		    borderwidth=0,
		    highlightthickness=0,
		    command=lambda: threading.Thread(target=decrease_volume_thread).start(),#lambda: print("button_7 clicked"),
		    relief="flat"
		)
		self.button_7.place(
		    x=686.0,
		    y=136.0,
		    width=58.0,
		    height=60.0
		)

	def fn(self):
		if self.flag==1:
			self.stop=True
		self.parent.update_frame()

	def speak(self):
		q=queue.Queue()

		#print("Hi, My Name is Jarvis and I will be your voice assistant",engine)
		#print("How may I address you?",engine)
		print("Hi",engine)
		user_name,flag="Arbaz",False
		while flag:
			user_name=get_name()
			user_name=user_name.split()[-1]
			print(user_name)
			engine.print(f"Is it, {user_name}?")
			engine.runAndWait()

			res=verify_name()

			flag=False if "yes" in res else True

			if flag:
				print("Could you please say your name, again?")



		say(f"Hello, {user_name}. Nice to meet you",engine)
		say("How may I help you?",engine)
		in_main_fn=True
		while True:

			with sd.RawInputStream(samplerate=sample_rate, blocksize = 8000, device=1, dtype='int16',channels=1, callback=lambda indata, frames, time, status: callback(indata, frames, time, status,q,in_main_fn)):
				if self.stop:
					print("ForceFull exit")
					break

				rec = vosk.KaldiRecognizer(model, sample_rate)

				text=None
				while text is None or text=="":
					data = q.get()
					if rec.AcceptWaveform(data):
						res=rec.Result()
						print(res)
						text=json.loads(res)["text"].lower()

				fn=None
				for phrase in COMMANDS:
					if any(word in text for word in phrase.split(",")) and (phrase!="google" or "meet" not in text):
						fn=COMMANDS[phrase]
						break

				if fn is not None:
					in_main_fn=False
					fn(text,engine,r)
					say("Command executed succesfully, Is there anything else I can help you out with?",engine)
					in_main_fn=True
				elif "stop" in text:
					break
				else:
					in_main_fn=False
					say("Couldn't recognize your command",engine)
					in_main_fn=True

		if self.parent.current_frame==self:
			self.parent.update_frame()

			




app=TkinterApp()
app.get_frames()		
app.mainloop()


