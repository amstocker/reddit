import pygame
from pygame.locals import *
import os
import csv
from sys import argv

# pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
w, h = 1024, 768
bg_color = (255,236,217)
cx, cy = w/2, h/2

pygame.init()
screen = pygame.display.set_mode((w, h))
screen.fill(bg_color)
pygame.display.flip()

eraser = pygame.Surface((w, h))
eraser.fill(bg_color)
eraser.set_alpha(10)

tracking = {}

def render_user(p, color):
    pygame.draw.circle(screen, (0,0,0), p, 5)
    pygame.draw.circle(screen, color, p, 4)

f = open(argv[1], "r")
reader = csv.reader(f)
for actions in reader:
    screen.blit(eraser, (0,0))
    index = 0
    length = len(actions)
    while index < length:
        action = actions[index]
        if action == 'new':
            exec('tracking[actions[index+1]] = ' + actions[index+2])
            index += 3
        else:
            exec('pos = ' + actions[index+1])
            dest = (int(cx+pos[0]), int(cy+pos[1]))
            render_user(dest, tracking[action])
            index += 2
    pygame.display.flip()

f.close()

done = False
while done == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

pygame.quit()


    
