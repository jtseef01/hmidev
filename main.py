import kivy
kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label as CoreLabel
from kivy.core.window import Window
Window.size = (800, 480)
class HomeScreen(Screen):
    def search_btn_pressed(self, btn_pressed):
      print btn_pressed.text

class CustomLayout(GridLayout):
	pass
	
class buttons_pressedApp(App):

    def build(self):

        return HomeScreen()

if __name__ == '__main__':
    buttons_pressedApp().run()
