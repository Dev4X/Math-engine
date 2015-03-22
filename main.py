from kivy.app import App
from kivy.uix.widget import Widget

__version__ = '0.1'

class PongApp(App):
    def build(self):
        return PongGame()

class PongGame(Widget):
    pass

if __name__ == "__main__":
    PongApp().run()

