from random import randint

class Apple:
    def __init__(self):
        self.pos = ()
    

    def spawn_apple(self, snake, screensize):
        h, w = screensize
        while True:
            pos = (randint(1, h - 2), randint(1, w - 2))
            if pos not in snake:
                self.pos = pos
                break 
