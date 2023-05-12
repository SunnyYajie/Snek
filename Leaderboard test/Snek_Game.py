import sqlite3
import datetime
import os, sys
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '800')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.resources import resource_add_path, resource_find
from kivy.uix.label import Label

class MyLayout(Widget):
     def backbutton (self):
          self.ids.bak_btn.text = '[color=#00ffcc]Info[/color]'
          self.ids.bak_btn.markup = True
class Snek(App):
    title = "Snek"
    def build(self):
            pass
            return MyLayout()  
    
        
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Snek().run()