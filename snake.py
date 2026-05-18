class Snake:
    def __init__(self, start: tuple, direction: tuple, collision :bool):
        self.start = start
        self.direction = direction
        self.collision = collision
        self.snake_color = 1
        self.snake_body = [start]
    
    def move(self):
        y, x = self.snake_body[0]
        dy, dx = self.direction
        return (y + dy, x + dx)

    def wrap_head(self, head, screensize):
        h, w = screensize
        y, x = head

        if y <= 0:
            y = h - 2
        elif y >= h - 1:
            y = 1

        if x <= 0:
            x = w - 2
        elif x >= w - 1:
            x = 1

        return (y, x)

    def isCollision(self, head, screensize):
        h, w = screensize
        y, x = head
        if y <= 0 or y >= h - 1 or x <= 0 or x >= w - 1:
            return True
        if head in self.snake_body:
            return True
        return False
        
