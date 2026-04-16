

class Snake:
    def __init__(self, start: tuple, direction: tuple):
        self.start = start
        self.direction = direction
        self.snake_color = 1
        self.snake_body = [start]

        
