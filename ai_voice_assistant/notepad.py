from pywinauto.application import Application
from pywinauto import keyboard
from dependency_assets import *

def notepad():
	app = Application().start("notepad.exe")
	#app.UntitledNotepad.print_control_identifiers()
	#diag = app.UntitledNotepad.child_window(title="Untitled - Notepad", control_type="Window").wrapper_object()
	while True:
		data=input("Your note: ")
		app.UntitledNotepad.Edit.type_keys(data, with_spaces = True)
		keyboard.send_keys('{ENTER}')

		flag=input("Would you like to save and exit y/n: ")
		if flag=="y":
			break
				
	app.UntitledNotepad.Edit.type_keys("Hello World!")
	keyboard.send_keys("^+s")
	dlg = app.window(title='Save As')
	dlg.Edit.type_keys("kushan")
	dlg.Save.click()
	dlg.Save.click()


def verify_file_name(text):
	say(f"is it {text}?",engine)

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

def write_text_in_notepad(text,engine,r):	#For braille keyboards use only #Comment part# rest is not required 
	say("Opening Notepad",engine)
	app = Application().start("notepad.exe")

	with sr.Microphone as source:
		r.adjust_for_ambient_noise(source)
		audio=r.listen(source)

		while True:
			text=r.recognize_google(audio,language = 'en-IN', show_all = True)['alternative'][0]['transcript'].lower()
			app.UntitledNotepad.Edit.type_keys(text+"\n", with_spaces = True)

			say("Would you like to save and exit, say yes or no",engine)
			temp=r.recognize_google(audio,language = 'en-IN', show_all = True)['alternative'][0]['transcript'].lower()
			if temp=="yes":
				break

	app.UntitledNotepad.menu_select("File->Save As")
	dlg = app.window(title='Save As')

	file_name=None
	with sr.Microphone as source:
		r.adjust_for_ambient_noise(source)
		audio=r.listen(source)

		while True:
			text=r.recognize_google(audio,language = 'en-IN', show_all = True)['alternative'][0]['transcript'].lower()
			flag=verify_file_name(text)
			if flag:
				file_name=text+".txt"
				break

	dlg.Edit.type_keys(file_name)
	dlg.Save.click()
	dlg.Save.click()
	app.UntitledNotepad.menu_select("File->Exit")


def write_text_in_notepad_1():	#For braille keyboards use only #Comment part# rest is not required 
	say("Opening Notepad")
  #os.startfile('C:\Windows\notepad.exe')
	#say("Start Typing")
	file = open('f.txt', 'w')
	with sr.Microphone as source:
		r.adjust_for_ambient_noise(source)
		audio=r.listen(source)
		flag = 1
		while flag:
			text=r.recognize_google(audio,language = 'en-IN', show_all = True)['alternative'][0]['transcript'].lower()
			file.wirte(text)
			say("Do You want to Continue Say Yes OR No")
			temp=r.recognize_google(audio,language = 'en-IN', show_all = True)['alternative'][0]['transcript'].lower()
			if temp=="no":
				flag=0
