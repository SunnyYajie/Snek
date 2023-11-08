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
from kivy.uix.screenmanager import ScreenManager, Screen
import time
import os
import sqlite3

#Window.size = 600, 800

########################
#Window and sprite size#
########################
SPRITE_SIZE = sp(20)
COLS = int(Window.width/ SPRITE_SIZE)
ROWS = int(Window.height/ SPRITE_SIZE)


LENGTH = 4
MOVESPEED = .087
ALPHA = .5


LEFT = 'left'
UP = 'up'
RIGHT = 'right'
DOWN = 'down'

BING = 1

CHECKER = 0

direction_values = {LEFT: [-1, 0], 
                    UP: [0, 1], 
                    RIGHT: [1, 0], 
                    DOWN: [0, -1]}

direction_group = {LEFT: 'horizontal',
                   UP: 'vertical',
                   RIGHT: 'horizontal',
                   DOWN: 'vertical'}

direction_keys = {'a': LEFT,
                  'w': UP,
                  'd': RIGHT,
                  's': DOWN}

class Sprite(Widget):
    coord = kp.ListProperty([0, 0])
    bgcolor = kp.ListProperty([0, 1, 0, 0])

SPRITES = defaultdict(lambda: Sprite())

class Fruit(Sprite):    
    pass
    
class Home(FloatLayout):
    pass

#####################
#Main Gameplay Class#
#####################
class Snake(App):
    score = kp.NumericProperty(0)
    sprite_size = kp.NumericProperty(SPRITE_SIZE)
    
    head = kp.ListProperty([0, 0])
    snake = kp.ListProperty()
    length = kp.NumericProperty(LENGTH)
    
    fruit = kp.ListProperty([0, 0])
    fruit_sprite = kp.ObjectProperty(Fruit)
    
    direction = kp.StringProperty(RIGHT, options = (LEFT, UP, RIGHT, DOWN))
    buffer_direction = kp.StringProperty(RIGHT, options = (LEFT, UP, RIGHT, DOWN, ''))
    block_input = kp.BooleanProperty(True)
    
    alpha = kp.NumericProperty(0)
    
    checker = kp.NumericProperty(CHECKER)
    #############
    #Swipe Input#
    #############
    def swipe_handler(self, instance, touch, *args):
        dx = touch.x - touch.opos[0]
        dy = touch.y - touch.opos[1]
        try:
            if abs(dx) > abs(dy):
                if dx > 0:
                    self.try_change_direction(RIGHT)
                else:
                    self.try_change_direction(LEFT)
            else:
                if dy > 0:
                    self.try_change_direction(UP)
                else:
                    self.try_change_direction(DOWN)
        except KeyError:
            pass
    
    ###################
    #Start of Gameplay#
    ###################
    def game_start(self):
        self.root.ids.scores.text = "0"
        self.root.ids.scores1.text = "0"
        self.root.ids.scores2.text = "0"
        self.fruit_sprite = Fruit()
        self.head = self.new_head_location
        self.fruit = self.new_fruit_location
        self.length = LENGTH
        self.checker += 1
        Clock.schedule_interval(self.move, MOVESPEED)
        Clock.unschedule(self.clear_snake)
        self.score = 0
        Window.bind(on_touch_up = self.swipe_handler)
        Window.bind(on_keyboard = self.key_handler)
    
    def on_fruit(self, *args):
        if not self.fruit_sprite.parent:
            self.root.add_widget(self.fruit_sprite)
        self.fruit_sprite.coord = self.fruit
        
    def key_handler(self, _, __, ____, key, *_____):
        try:
            self.try_change_direction(direction_keys[key])
        except KeyError:
            pass
        
    def try_change_direction(self, new_direction):    
        if direction_group[new_direction] != direction_group[self.direction]:
            if self.block_input:
                self.buffer_direction = new_direction
            else:    
                self.direction = new_direction
                self.block_input = True
        
    def on_head(self, *args):
        self.snake.append(self.head)
        self.snake = self.snake[-self.length:] + [self.head]
        
    def on_snake(self, *args):
        for index, coord in enumerate(self.snake):
            sprite = SPRITES[index]
            sprite.coord = coord
            if not sprite.parent:
                self.root.add_widget(sprite)
    
    @property
    def new_head_location(self):
        return [randint(2, dim - 2) for dim in [COLS, ROWS]]
    
    @property
    def new_fruit_location(self):
        while True:
            fruit = [randint(0, dim - 1) for dim in [COLS, ROWS]]
            if fruit not in self.snake and fruit != self.fruit:
                return fruit
    
    def move(self, *args):
        new_head = [sum(x) for x in zip(self.head, direction_values[self.direction])]

        if new_head in self.snake:
            self.head = [-100, 0]
            self.block_input = True
            return self.die()

    
        if not self.check_inbounds(new_head):
            self.block_input = True
            return self.die()

        
        if new_head == self.fruit:
            self.fruit = self.new_fruit_location
            self.length += 1
            self.score += 1
            self.root.ids.scores.text = str(int(self.root.ids.scores.text) + 1)
            self.root.ids.scores1.text = str(int(self.root.ids.scores1.text) + 1)
            self.root.ids.scores2.text = str(int(self.root.ids.scores2.text) + 1)
            
        if self.buffer_direction:
            self.try_change_direction(self.buffer_direction)
            self.buffer_direction = ''
        
        self.head = new_head
        self.block_input = False
    
    def check_inbounds(self, pos):
        return all(0 <= pos[x] < dim for x, dim in enumerate([COLS, ROWS]))
    
    def if_highscore(self, *args):
        inp_name = self.root.ids.username.text
        inp_score = self.root.ids.scores.text
        dbconn = sqlite3.connect("leaderboard.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        dbcursor.execute(
            "INSERT INTO leaderboardtable (name, highscore) VALUES (:var_name, :var_highscore)", 
            {
                'var_name' : inp_name,
                'var_highscore' : inp_score,
            })
        dbconn.commit()
        dbconn.close()
        
    def check_score(self, *args):
        dbconn = sqlite3.connect("leaderboard.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        dbcursor.execute("SELECT * FROM leaderboardtable ORDER BY highscore DESC LIMIT 5;")
        record = dbcursor.fetchall()
        if len(record) >= 1:
            self.root.ids.OneName.text = record[0][0]
            self.root.ids.OneScore.text = str(record[0][1])
        else:
            self.root.ids.OneName.text = "---"
            self.root.ids.OneScore.text = "---"
            
        if len(record) >= 2:
            self.root.ids.TwoName.text = record[1][0]
            self.root.ids.TwoScore.text = str(record[1][1])
        else:
            self.root.ids.TwoName.text = "---"
            self.root.ids.TwoScore.text = "---"
        
        if len(record) >= 3:
            self.root.ids.ThreeName.text = record[2][0]
            self.root.ids.ThreeScore.text = str(record[2][1])
        else:
            self.root.ids.ThreeName.text = "---"
            self.root.ids.ThreeScore.text = "---"
        
        if len(record) >= 4:
            self.root.ids.FourName.text = record[3][0]
            self.root.ids.FourScore.text = str(record[3][1])
        else:
            self.root.ids.FourName.text = "---"
            self.root.ids.FourScore.text = "---"
        
        if len(record) >= 5:
            self.root.ids.FiveName.text = record[4][0]
            self.root.ids.FiveScore.text = str(record[4][1])
        else:
            self.root.ids.FiveName.text = "---"
            self.root.ids.FiveScore.text = "---"
        
        dbconn.commit()
        dbconn.close()
        
    def on_death(self, *args):
        dbconn = sqlite3.connect("leaderboard.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        dbcursor.execute("SELECT * FROM leaderboardtable ORDER BY highscore DESC LIMIT 5;")
        record = dbcursor.fetchall()
        if int(self.root.ids.scores1.text) > record[0][1]:
            self.root.ids.screen_manager.current = "highscore_screen"
            self.root.ids.screen_manager.transition.direction = "up"
        else:
            self.root.ids.screen_manager.current = "gameover_screen"
            self.root.ids.screen_manager.transition.direction = "down"
        dbconn.commit()
        dbconn.close()
            
    def clear_snake(self, *args):
        self.snake.clear()
        excempt_widgets = [self.root.ids.screen_manager]
        children = self.root.children
        for child in children:
            if child not in excempt_widgets:
                self.root.remove_widget(child)
        
    def unsched_snake(self):
        Clock.unschedule(self.clear_snake)
    
    def die(self):
        self.root.ids.StartButton.disabled = False
        self.root.ids.StartButton.opacity = 1
        self.alpha = ALPHA
        self.length = 0
        self.on_death()
        Clock.unschedule(self.move)
        Clock.schedule_interval(self.clear_snake, 0.085)
        
        
        
        
        
    def build(self):
        return Home()

if __name__ == '__main__':
    Snake().run()