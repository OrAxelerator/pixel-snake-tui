class Snake:
    def __init__(self, start: tuple, direction: tuple):
        self.start = start
        self.direction = direction
        self.snake_color = 1
        self.snake_body = [start]
    
    def move(self):
        y, x = self.snake_body[0]
        dy, dx = self.direction
        return (y + dy, x + dx)

    def colision(self, head, screenzise):
        h, w = screenzise
        y, x = head
        if y <= 0 or y >= h - 1 or x <= 0 or x >= w - 1:
            return True
        if head in self.snake_body:
            return True
        return False
        
