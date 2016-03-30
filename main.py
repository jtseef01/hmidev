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
import time
Window.size = (800, 480)

##################################################################################
## initialization code
##################################################################################
ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)
screen_manager = None
q = Queue()
EXIT = 0    

class SimSerial():
	global q
	def __init__(self, queue):
		self.q = queue

	def put_on_queue(self):
		global EXIT
		while EXIT == 0:
			print ser.readline()


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
	def build(self):
		screen_manager = ScreenManager(transition=NoTransition())
		screen_manager.add_widget(Dashboard(name='dash'))
		screen_manager.add_widget(MotorGotoScreen(name='gotomotor'))
		Clock.schedule_interval(self.get_from_queue, 1.0)
		return screen_manager
	 
	def get_from_queue(self, dt):
		print("---------> ShowGUI.get_from_queue() entry")
		try:
			queue_data = q.get_nowait()
			text = ''
			for qd in queue_data:
				if(qd != '\n'):
					text += qd
				else:
					print("SimKivy.get_from_queue(): got data from queue: " + text)
					text = ''
		except Empty:
			print("No data received on queue.")
			return

if __name__ == '__main__':
	global q
	ss = SimSerial(q)

	simSerial_thread = Thread(name="simSerial",target=ss.put_on_queue)
	simSerial_thread.start()

	print("Starting KivyGui().run()")

	buttons_pressedApp().run()

