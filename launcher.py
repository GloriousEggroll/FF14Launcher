#!/usr/bin/env python3
# FFXIV ARR Python Launcher - Python 2 or 3
# Author: Jordan Henderson
# This is a fairly quick and nasty implementation of a functional launcher for FFXIV.
# TODO: ffxivupdate support.
# refactoring and changes: Matthew Clark, Arthur Moore, Stian E. Syvertsen



from getpass import getpass
from login import *
if (sys.version_info >= (3,0)):
	from configparser import ConfigParser
else:
	from ConfigParser import ConfigParser

def gen_launcher_string(settings):
	launcher_str = '{wine_command}' \
		+' \'{path}/game/ffxiv.exe\'' \
		+' "language=1"' \
		+' "DEV.UseSqPack=1" "DEV.DataPathType=1"' \
		+' "DEV.LobbyHost01=neolobby01.ffxiv.com" "DEV.LobbyPort01=54994"' \
		+' "DEV.LobbyHost02=neolobby02.ffxiv.com" "DEV.LobbyPort02=54994"' \
		+' "DEV.TestSID={actual_sid}"' \
		+' "DEV.MaxEntitledExpansionID={expansion_id}"' \
		+' "SYS.Region={region}"' \
		+' "ver={version}"'
	return launcher_str.format(**settings)

def run(settings):
	sid=login(settings['region'],settings['user'],settings['password'],settings['one_time_password'])
	(settings['actual_sid'],settings['version']) = get_actual_sid(sid,settings['path'])
	launch = gen_launcher_string(settings)
	print(launch)
	os.system(launch)

def run_cli(settings):
	if (settings['user'] == ''):
		settings['user'] = raw_input("User Name:  ")
	if (settings['password'] == ''):
		settings['password'] = getpass()
	try:
		run(settings)
	except Exception as err:
		print("Error:  " + str(err))

class gui_prompt:
	def run_gui(self):
		#Store the user input
		settings['user']=self.E1.get();
		settings['password']=self.E2.get();
		settings['one_time_password']=self.E3.get()
		#Disable the GUI
		self.top.quit()
		self.top.destroy()
		#Run the Program
		try:
			run(settings)
		except Exception as err:
			if (sys.version_info >= (3,0)):
				import tkinter
				from tkinter.messagebox import showwarning
			else:
				import Tkinter as tkinter
				from tkMessageBox import showwarning
			top = tkinter.Tk()
			top.wm_withdraw()
			showwarning("Error", str(err), parent=top)

	def __init__(self,settings):
		if (sys.version_info >= (3,0)):
			import tkinter
		else:
			import Tkinter as tkinter
		self.top = tkinter.Tk()

		self.L1 = tkinter.Label(self.top, text="User Name")
		self.L1.grid(row = 0, column = 0)
		self.E1 = tkinter.Entry(self.top, textvariable=tkinter.StringVar(value=settings['user']))
		self.E1.grid(row = 0, column = 1)
		self.L2 = tkinter.Label(self.top, text="Password")
		self.L2.grid(row = 1, column = 0)
		self.E2 = tkinter.Entry(self.top, show="*", textvariable=tkinter.StringVar(value=settings['password']))
		self.E2.grid(row = 1, column = 1)
		self.L3 = tkinter.Label(self.top, text="One Time Password")
		self.L3.grid(row = 2, column = 0)
		self.E3 = tkinter.Entry(self.top, textvariable=tkinter.StringVar(value=settings['one_time_password']))
		self.E3.grid(row = 2, column = 1)

		self.OK = tkinter.Button(self.top, text ="Connect", command = self.run_gui)
		self.OK.grid(row = 3, column = 1)
		self.top.bind('<Return>', lambda _: self.OK.invoke())
		self.top.bind('<KP_Enter>', lambda _: self.OK.invoke())

		#Place window in center of screen
		self.top.eval('tk::PlaceWindow %s center' % self.top.winfo_pathname(self.top.winfo_id()))
		#Focus on the one time password box at start
		self.E3.focus()
		self.top.title("FFXIV Launcher")
		self.top.mainloop()

config_path=os.path.dirname(os.path.realpath(sys.argv[0]))
config = ConfigParser()
config.read(config_path+'/launcher_config.ini')
settings = config._sections['FFXIV']

if len(sys.argv) > 1:
	settings['one_time_password'] = sys.argv[1]

if (config['FFXIV'].getboolean('USEGUI')):
	gui_prompt(settings)
else:
	run_cli(settings)
