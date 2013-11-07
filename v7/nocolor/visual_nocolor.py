import pygame
from pygame.locals import *
import os
import csv
from sys import argv

# pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
w, h = 1024, 768
bg_color = (0,0,0)
cx, cy = w/2, h/2

pygame.init()
screen = pygame.display.set_mode((w, h))
screen.fill(bg_color)
pygame.display.flip()

font = pygame.font.SysFont(None, 20, bold=False, italic=False)

eraser = pygame.Surface((w, h))
eraser.fill(bg_color)
eraser.set_alpha(15)

tracking = {}

def render_user(p):
    pygame.draw.circle(screen, (0,0,0), p, 6)
    pygame.draw.circle(screen, (0,255,0), p, 5)

f = open(argv[1], "r")
reader = csv.reader(f)
for actions in reader:
    screen.blit(eraser, (0,0))
    index = 1
    tstr = actions[0]
    length = len(actions)
    while index < length:
            exec('pos = ' + actions[index])
            dest = (int(cx+pos[0]), int(cy+pos[1]))
            render_user(dest)
            index += 1
    pygame.draw.rect(screen, (0,0,0), [0,0,190,23])
    screen.blit(font.render(tstr, False, (255,255,255)), (5,5))
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


    
