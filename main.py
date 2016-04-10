#########################################
##Authors: Jared Seeforth; Logan Hall
#########################################

import serial
import kivy
import sys
from threading import Thread
from Queue import Queue, Empty
kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label as CoreLabel
from kivy.core.window import Window
from kivy.clock import Clock
import datetime
from datetime import timedelta
Window.size = (800, 480)

##################################################################################
## initialization code
##################################################################################
ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)
q = Queue()
EXIT = 0    

class SimSerial():
	global q
	def __init__(self, queue):
		self.q = queue

	def put_on_queue(self):
		global EXIT
		potent_counter = 0
		pass_thru = 'glproc'
		potent_vals = 'witbv'
		last_rcv = 'z'
		while EXIT == 0:
			self.text = ser.readline()
			if(len(self.text) > 0):
				if(self.text[0] != last_rcv[0] and last_rcv[0] in potent_vals):
					self.q.put(last_rcv)
				
				if(self.text[0] in pass_thru):
					self.q.put(self.text)
				
				else:
					potent_counter += 1
					if(potent_counter >= 10):
						self.q.put(self.text)
						potent_counter = 0
				last_rcv = self.text

##################################################################################
## GUI CODE
##################################################################################
class Dashboard(Screen):
	def search_btn_pressed(self, btn_pressed):
		global EXIT
		if(btn_pressed.text == 'Close Door'):
			ser.write('c')
		elif(btn_pressed.text == 'Open Door'):
			ser.write('o')
		elif(btn_pressed.text == 'Servo Loosen'):
			ser.write('l')
		elif(btn_pressed.text == 'Servo Grip'):
			ser.write('g')
		elif(btn_pressed.text == 'Play'):
			ser.write('p')
		elif(btn_pressed.text == 'Reset'):
			ser.write('r')
		elif(btn_pressed.text == 'Exit'):
			EXIT = 1
			sys.exit()
			
			

class MotorGotoScreen(Screen):
	def search_btn_pressed(self, btn_pressed):
		if(btn_pressed.text == '>>'):
			if(self.ids.slider_id.value < self.ids.slider_id.max):
				self.ids.slider_id.value += 1
		elif(btn_pressed.text == '<<'):
			if(self.ids.slider_id.value > self.ids.slider_id.min):
				self.ids.slider_id.value -= 1
		elif(btn_pressed.text == "Submit Command"):
			text = ''
			val = str(int(self.ids.slider_id.value))
			if(self.ids.wrist_btn.state == 'down'):
				text = 'w' + val
				self.ids.wrist_btn.state = 'normal'
			elif(self.ids.base_btn.state == 'down'):
				text = 'b' + val
				self.ids.base_btn.state = 'normal'
			elif(self.ids.telescopic_btn.state == 'down'):
				text = 't' + val
				self.ids.telescopic_btn.state = 'normal'
			elif(self.ids.ignitor_btn.state == 'down'):
				text = 'i' + val
				self.ids.ignitor_btn.state = 'normal'
			elif(self.ids.vas_btn.state == 'down'):
				text = 'v' + val
			self.ids.vas_btn.state = 'normal'
			if(text != ''):
				ser.write(text)
			self.manager.current = 'dash'
			
class CustomLayout(GridLayout):
	pass
               
class buttons_pressedApp(App):
	global q
	screen_manager = None
	dash = None
	def build(self):
		screen_manager = ScreenManager(transition=NoTransition())
		screen_manager.add_widget(Dashboard(name='dash'))
		self.dash = screen_manager.get_screen('dash')
		screen_manager.add_widget(MotorGotoScreen(name='gotomotor'))
		Clock.schedule_interval(self.get_from_queue, .001)
		return screen_manager
	 
	def get_from_queue(self, dt):
		try:
			data_rcv = q.get_nowait()
			print '[DEBUG] data from queue: ' + data_rcv
			data_rcv = data_rcv.replace('\n', '\0')
			data_rcv = data_rcv.replace('\r', '\0')		
			char = data_rcv[0]
			
			if 'p' in data_rcv:
				self.dash.ids.state_val.text = 'Paused'
				return

			if(char == 'o'):
				self.dash.ids.door_val.text = 'Open'
			elif(char == 'c'):
				self.dash.ids.door_val.text = 'Closed'
			elif(char == 'r'):
				self.dash.ids.state_val.text = 'Running'
			elif(char == 'w'):
				self.dash.ids.wrist_potent_val.text = data_rcv[1:]
			elif(char == 't'):
				self.dash.ids.tele_potent_val.text = data_rcv[1:]
			elif(char == 'b'):
				self.dash.ids.base_potent_val.text = data_rcv[1:]
			elif(char == 'i'):
				self.dash.ids.ignitor_potent_val.text = data_rcv[1:]
			elif(char == 'v'):
				self.dash.ids.vas_potent_val.text = data_rcv[1:]
		except Empty:
			return
if __name__ == '__main__':
	ss = SimSerial(q)

	simSerial_thread = Thread(name="simSerial",target=ss.put_on_queue)
	simSerial_thread.start()

	buttons_pressedApp().run()

