from vector import *
import pygame
import math

def map_(x, min1, max1, min2, max2):
    per = (x - min1) / (max1 - min1)
    new = per * (max2 - min2)
    return new + min2

def constrain(x, min_):
    if x < min_:
        x = min_
    return x

class Cell:
    def __init__(self, pos):
        self.pos = Vector(pos[0], pos[1])
        self.width = cell_width
        self.E = 0

    def update_E(self, sources):
        x = self.pos.x * self.width + self.width // 2
        y = self.pos.y * self.width + self.width // 2
        pos = Vector(x, y)
        E = 0
        for source in sources:
            source_pos = source.pos * self.width + Vector(self.width // 2, self.width // 2)
            distance = self.pos.dist(source.pos) / 10

            E += math.cos(source.k * distance - source.omega * t + source.phase) / constrain(distance, 1)

        self.E = E

    def update_col(self, max_val):
        col = round(map_(self.E**2, 0, max_val, 0, 255))
        self.col = (col, col, col)

    def display(self, win):
        pygame.draw.rect(win, self.col, (self.pos.x * self.width, self.pos.y * self.width, self.width, self.width))

class Source:
    def __init__(self, pos, k, omega, phase):
        self.pos = Vector(pos[0], pos[1])
        self.phase = phase
        self.k = k
        self.omega = omega

    def display(self, win):
        pygame.draw.circle(win, (255, 0, 0), (self.pos.x * cell_width + cell_width // 2, self.pos.y * cell_width + cell_width // 2), cell_width // 2)


pygame.init()

width = 500
height = 500

fps = 60

k = 5
omega = 15

cell_width = 10

rows = height // cell_width
cols = width // cell_width

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Wave superposition simulation")
clock = pygame.time.Clock()

grid = [[Cell([i, j]) for i in range(cols)] for j in range(rows)]

for i in range(cols):
    for j in range(rows):
        grid[j][i].update_col(1)

sources = []

t = 0
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x = mouse_pos[0] // cell_width
            y = mouse_pos[1] // cell_width

            repeat = False
            for i in range(len(sources)):
                if sources[i].pos.equals(Vector(x, y)):
                    del sources[i]
                    repeat = True
                    break

            if not repeat:
                sources.append(Source([x, y], k, omega, -omega * t))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                for source in sources:
                    source.phase = 0


    win.fill((255, 255, 255))

    for i in range(cols):
        for j in range(rows):
            grid[j][i].value = 0

    for i in range(cols):
        for j in range(rows):
            grid[j][i].update_E(sources)
            if len(sources) > 0:
                grid[j][i].update_col(len(sources)**2)
            else:
                grid[j][i].update_col(1)
            grid[j][i].display(win)

    for source in sources:
        source.display(win)

    t += 1 / fps

    pygame.display.update()
    clock.tick(fps)

pygame.quit()