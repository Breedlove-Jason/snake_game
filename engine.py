"""Shared, display-independent rules for desktop and browser Snake."""
import json
import random

DIRECTIONS = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}


class Game:
    def __init__(self, size=24, rng=None):
        if size < 4:
            raise ValueError('Board must be at least four cells wide')
        self.size = size
        self.rng = rng or random.Random()
        self.reset()

    def reset(self):
        mid = self.size // 2
        self.snake = [(mid, mid), (mid - 1, mid), (mid - 2, mid)]
        self.direction = 'right'
        self.pending = None
        self.score = 0
        self.status = 'ready'
        self.food = self.spawn_food()

    def spawn_food(self):
        occupied = set(self.snake)
        free = [(x, y) for y in range(self.size) for x in range(self.size)
                if (x, y) not in occupied]
        return self.rng.choice(free) if free else None

    def start(self):
        if self.status in ('ready', 'paused'):
            self.status = 'running'

    def pause(self):
        if self.status == 'running':
            self.status = 'paused'

    def turn(self, direction):
        if self.status != 'running' or direction not in DIRECTIONS or self.pending:
            return False
        old, new = DIRECTIONS[self.direction], DIRECTIONS[direction]
        if direction == self.direction or (old[0] + new[0], old[1] + new[1]) == (0, 0):
            return False
        self.pending = direction
        return True

    def step(self):
        if self.status != 'running':
            return
        self.direction = self.pending or self.direction
        self.pending = None
        dx, dy = DIRECTIONS[self.direction]
        x, y = self.snake[0]
        head = (x + dx, y + dy)
        eating = head == self.food
        body = self.snake if eating else self.snake[:-1]
        if not (0 <= head[0] < self.size and 0 <= head[1] < self.size) or head in body:
            self.status = 'over'
            return
        self.snake.insert(0, head)
        if eating:
            self.score += 1
            self.food = self.spawn_food()
            if self.food is None:
                self.status = 'won'
        else:
            self.snake.pop()

    def snapshot(self):
        return json.dumps(dict(size=self.size, snake=self.snake, food=self.food,
                               direction=self.direction, score=self.score, status=self.status))
