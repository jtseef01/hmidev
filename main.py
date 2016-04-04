import serial
import kivy
import sys
kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label as CoreLabel
from kivy.core.window import Window
Window.size = (800, 480)

##################################################################################
## initialization code
##################################################################################
#ser = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout = 1)

##################################################################################
## serial listen function
##################################################################################

def serial_listen(dash): 
	data_rcv = ''
	print dash.name
	while(data_rcv != 'p'):
		data_rcv = ser.readline()
		data_rcv = data_rcv.replace('\n', '\0')
		data_rcv = data_rcv.replace('\r', '\0')
		
		char = text[0]
		if(char == 'o'):
			dash.ids.door_val.text = 'Open'
		elif(char == 'c'):
			dash.ids.door_val.text = 'Closed'
		elif(char == 'r'):
			dash.ids.state_val.text = 'Running'
		elif(char == 'w'):
			dash.ids.wrist_potent_val.text = data_rcv[1:]
		elif(char == 't'):
			dash.ids.tele_potent_val.text = data_rcv[1:]
		elif(char == 'b'):
			dash.ids.base_potent_val.text = data_rcv[1:]
		elif(char == 'i'):
			dash.ids.ignitor_potent_val.text = data_rcv[1:]
		elif(char == 'v'):
			dash.ids.vas_potent_val.text = data_rcv[1:]
		
	dash.ids.state_val.text = 'Paused'
		
		

##################################################################################
## GUI CODE
##################################################################################
class Dashboard(Screen):
	def search_btn_pressed(self, btn_pressed):
		global EXIT
		if(btn_pressed.text == 'Close Door'):
			print 'c'
			#ser.write('c')
		elif(btn_pressed.text == 'Open Door'):
			print 'o'
			#ser.write('o')
		elif(btn_pressed.text == 'Servo Loosen'):
			print 'l'
			#ser.write('l')
		elif(btn_pressed.text == 'Servo Grip'):
			print 'g'
			#ser.write('g')
		elif(btn_pressed.text == 'Play'):
			print 'p'
			#ser.write('p')
		elif(btn_pressed.text == 'Reset'):
			print 'r'
			#ser.write('r')
		elif(btn_pressed.text == 'Exit'):
			EXIT = 1
			sys.exit()
		serial_listen(self)
			
			

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
				serial_listen(self.get_screen('dash'))
			self.manager.current = 'dash'
			
class CustomLayout(GridLayout):
	pass
               
class buttons_pressedApp(App):
	def build(self):
		screen_manager = ScreenManager(transition=NoTransition())
		screen_manager.add_widget(Dashboard(name='dash'))
		screen_manager.add_widget(MotorGotoScreen(name='gotomotor'))
		return screen_manager
	 
if __name__ == '__main__':
	buttons_pressedApp().run()

