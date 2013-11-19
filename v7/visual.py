import pygame
from pygame.locals import *
import os
import csv
from sys import argv

# pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
w, h = 1024, 768
bg_color = (0,0,255)
cx, cy = (w/2)-6, (h/2)-6

pygame.init()
screen = pygame.display.set_mode((w, h))
screen.fill(bg_color)
pygame.display.flip()

font = pygame.font.SysFont(None, 20, bold=False, italic=False)

eraser = pygame.Surface((w, h))
eraser.fill(bg_color)
eraser.set_alpha(2)

# resolution-1 must be evenly divisible into 255
resolution = 86
inc = 255/(resolution-1)
clist = [(255-inc*i, 0+inc*i, 0) for i in xrange(resolution)]
surflist = [0]*resolution
for i in xrange(resolution):
    A = pygame.Surface((12,12))
    A.fill((255,255,255))
    A.set_colorkey((255,255,255))
    pygame.draw.circle(A, (0,0,0), (6,6), 6)
    pygame.draw.circle(A, clist[i], (6,6), 5)
    A.set_alpha(inc*i)
    surflist[i] = A

tracking = {}



f = open(argv[1], "r")
reader = csv.reader(f)
for actions in reader:
    #screen.blit(eraser, (0,0))
    index = 1
    tstr = actions[0]
    length = len(actions)
    while index < length:
        action = actions[index]
        if action == 'new':
            tracking[actions[index+1]] = 0
            index += 3
        else:
            exec('pos = ' + actions[index+1])
            screen.blit(surflist[min(resolution-1, tracking[action])], (int(cx+pos[0]), int(cy+pos[1])))
            tracking[action] += 1
            index += 2
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


    
