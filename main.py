import serial
import kivy
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
#port = serial.Serial("/dev/ttyAMA0", baudrate = 9600, timeout = 2)



##################################################################################
## GUI CODE
##################################################################################
class Dashboard(Screen):
    def search_btn_pressed(self, btn_pressed):
		print btn_pressed.text

class MotorGotoScreen(Screen):
	def search_btn_pressed(self, btn_pressed):
		if(btn_pressed.text == '>>'):
			if(self.ids.slider_id.value < self.ids.slider_id.max):
				self.ids.slider_id.value += 1
		elif(btn_pressed.text == '<<'):
			if(self.ids.slider_id.value > self.ids.slider_id.min):
				self.ids.slider_id.value -= 1
		elif(btn_pressed.text == "Submit Command"):
			print 'command submitted'
			self.manager.current = 'dash'
			
		
			
class TestScreen(Screen):
	pass

class CustomLayout(GridLayout):
	pass

class buttons_pressedApp(App):

    def build(self):
		sm = ScreenManager(transition=NoTransition())
		sm.add_widget(Dashboard(name='dash'))
		sm.add_widget(MotorGotoScreen(name='gotomotor'))
		return sm

if __name__ == '__main__':
    buttons_pressedApp().run()
