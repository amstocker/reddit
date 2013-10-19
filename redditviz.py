import pygame
from pygame.locals import *
import praw
from math import pi, cos, sin, sqrt
import time
from pprint import pprint
import os
# center window on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# pygame
pygame.init()
w, h = 1024, 768
screen = pygame.display.set_mode((w, h))
screen.fill((255,255,255))
pygame.display.flip()
done = False

# screen pos vars
cx, cy = w/2, h/2
# graph scalers
scale = 300
inc = .01

# praw
r = praw.Reddit('Reddit test script -- amstocker.wordpress.com')
thread = r.get_submission(
    submission_id = "1oo0ug",
    comment_limit = None
    )

# tracked a comment object
tracked_comments = {}

# tracked by username
tracked_users = {}

### -----FUNCTIONS-----

# function to increment node v1 towards node v2 by d
def increment(v1, v2, d):
    p = (v2[0]-v1[0], v2[1]-v1[1])
    s = d/sqrt(p[0]**2 + p[1]**2)
    p = (p[0]*s, p[1]*s)
    return (v1[0]+p[0], v1[1]+p[1])
    
# function to move users based on commenting
def increment_users(parent, comments, user_dict):
    for comment in comments:
        if comment.__class__.__name__ != 'MoreComments':
            user_dict[comment.author] = increment(
                user_dict[comment.author],
                user_dict[parent.author],
                inc
                )
            if len(comment.replies) > 0:
                increment_users(comment, comment.replies, user_dict)

# store data for all initially active users in a thread
def init_users(thread, user_dict):
    user_dict[thread.author] = (0,0)
    for comment in praw.helpers.flatten_tree(thread.comments):
        if comment.__class__.__name__ != 'MoreComments':
            user_dict[comment.author] = (0,0)
    size = len(user_dict)
    theta = 2*pi/size
    for i, user in enumerate(user_dict):
        user_dict[user] = (cos(i*theta), sin(i*theta))

def render_user(user_pos, scaler):
    c = (int(cx+scaler*user_pos[0]), int(cy+scaler*user_pos[1]))
    pygame.draw.circle(screen, (0,0,0), c, 6)
    pygame.draw.circle(screen, (240,46,113), c, 5)

init_users(thread, tracked_users)

### -----MAIN LOOP-----

while done == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                done = True

    increment_users(thread, thread.comments, tracked_users)

    # this line of code below clears the screen, but I'm commenting it
    # out in order to create a ghosting effect to show the movement
    # of the nodes.
    # screen.fill((255,255,255))
    
    for user in tracked_users:
        render_user(tracked_users[user], scale)
        
    pygame.display.flip()
    ## eventually need to time API calls here ---> time.sleep(30)


pygame.quit()
        
