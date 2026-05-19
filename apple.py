from random import randint, choices

class Apple:
    def __init__(self):
        self.pos = ()
        self.type = self.init_type()
    
    # gold = +2len
    # uranium = -2len (like poison)
    # gltich = inverse les controle pendant 5s

    def init_type(self):
        AppleType = ("normal", "gold", "glitch", "uranium")

        typ = choices(
            population=AppleType,
            weights=(65, 20, 5, 10),
            k=1
        )        
        return typ[0] # cause it's a array["string"]

    def spawn_apple(self, snake, screensize):
        h, w = screensize
        while True:
            pos = (randint(1, h - 2), randint(1, w - 2))
            if pos not in snake:
                self.pos = pos
                break 
