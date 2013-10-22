import pygame
from pygame.locals import *
import praw
from math import pi, cos, sin, sqrt
import random
import time
from pprint import pprint
import os
# center window on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# pygame
pygame.init()
w, h = 1024, 768
screen = pygame.display.set_mode((w, h))
screen.fill((255,236,217))
pygame.display.flip()
done = False

# screen pos vars
cx, cy = w/2, h/2
# unit increment quantity
inc = 30



### -----DATA-----

# tracked a comment object
tracked_comments = []
# tracked by username, stores history of positions in a list for drawing purposes
tracked_users = {}
user_colors = {}



### -----FUNCTIONS-----

def update_thread(reddit, thread_id):
    return reddit.get_submission(
        submission_id = thread_id,
        comment_limit = None
        )

# function to increment node v1 towards node v2 by d
def increment(v1, v2, d):
    p = (v2[0]-v1[0], v2[1]-v1[1])
    if p == (0, 0):
        return v1
    s = d/sqrt(p[0]**2 + p[1]**2)
    p = (p[0]*s, p[1]*s)
    return (v1[0]+p[0], v1[1]+p[1])
    
# function to move users based on commenting
def increment_users(parent, comments, user_dict, tracking_list, color_dict):
    for comment in comments:
        if comment.__class__.__name__ != 'MoreComments':
            if comment not in tracking_list:
                print "NEW COMMENT @", comment.author, "@", comment
                tracking_list.append(comment)
                if str(comment.author) not in user_dict:
                    print "NEW USER @", str(comment.author)
                    user_dict[str(comment.author)] = [(
                        random.uniform(-1*cx, cx),
                        random.uniform(-1*cy, cy)
                        )]
                    color_dict[str(comment.author)] = (
                        random.randint(0,255),
                        random.randint(0,255),
                        random.randint(0,255)
                        )
                else:
                    user_dict[str(comment.author)].insert(0, increment(
                        user_dict[str(comment.author)][0],
                        user_dict[str(parent.author)][0],
                        inc
                        ))
            if len(comment.replies) > 0:
                increment_users(comment, comment.replies, user_dict, tracking_list, color_dict)

# store data for initial thread starter
def init_parent(thread, user_dict, color_dict):
    user_dict[str(thread.author)] = [(
        random.uniform(-1*cx, cx),
        random.uniform(-1*cy, cy)
        )]
    color_dict[str(thread.author)] = (
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255)
        )

def render_user(pos, color):
    pygame.draw.circle(screen, (0,0,0), pos, 5)
    pygame.draw.circle(screen, color, pos, 4)

# need to optimize this to only draw new line and new node if i'm not refreshing the window,
# should probably integrate into increment users function?
def render_history(user_pos_list, color):
    length = len(user_pos_list)
    c = (int(cx+user_pos_list[length-1][0]), int(cy+user_pos_list[length-1][1]))
    render_user(c, color)
    i = length-2
    while i > -1:
        c_origin = (int(cx+user_pos_list[i+1][0]), int(cy+user_pos_list[i+1][1]))
        c_dest = (int(cx+user_pos_list[i][0]), int(cy+user_pos_list[i][1]))
        pygame.draw.line(screen, (0,0,0), c_origin, c_dest, 3)
        pygame.draw.line(screen, color, c_origin, c_dest, 1)
        render_user(c_dest, color)
        i -= 1



### -----MAIN-----
            
r = praw.Reddit('Reddit test script -- amstocker.wordpress.com')
thread = update_thread(r, "1owd6p")
init_parent(thread, tracked_users, user_colors)

while done == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                done = True

    thread = update_thread(r, "1owd6p")
    print "updated @",time.time()
    increment_users(
        thread,
        thread.comments,
        tracked_users,
        tracked_comments,
        user_colors
        )
    
    for user in tracked_users:
        render_history(tracked_users[user], user_colors[user])
        
    pygame.display.flip()
    time.sleep(10)


pygame.quit()
        
