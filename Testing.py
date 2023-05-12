import kivy
from kivy.metrics import sp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy import properties as kp
from kivy.uix.widget import Widget
from collections import defaultdict
from kivy.app import App
from kivy.animation import Animation
from random import randint
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

Window.size = 600, 800

class Home(FloatLayout):
    pass



class testing(App):
    def build(self):
        self.Home = Home()
        return Home()


if __name__ == '__main__':
    testing().run()
    