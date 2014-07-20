import kivy
# TODO kivy.require

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from comm import *

class PongGame(Widget):
    #def __init__(self):
        """  
        self.kgc = KeyGenerationCenter(1024,4)
        self.comunicator = Comm(self.kgc,4)
        self.comunicator.bucle()
        self.text = str(self.comunicator.messages[1])
        """
        pass


class PongApp(App):

    def build(self):

        return PongGame()

if __name__ == '__main__':
    PongApp().run()




