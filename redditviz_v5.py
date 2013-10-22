import pygame
from pygame.locals import *
import praw
from math import pi, cos, sin, sqrt
import random
import time
from pprint import pprint
import os

# pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
w, h = 1024, 768
cx, cy = w/2, h/2
screen = pygame.display.set_mode((w, h))
screen.fill((255,236,217))
pygame.display.flip()
done = False

# pygame Surface object to erase screen over time
eraser = pygame.Surface((w, h))
eraser.fill((255,236,217))
eraser.set_alpha(10)

# unit increment quantity
inc = 4


### -----DATA-----

# dictionary of tracked threads and tracked comments within that thread
tracked_threads = {}
# queue of threads to update
tracked_threads_queue = []
# dictionary of users and their current positions
tracked_users = {}
# dictionary of users and their color representation
tracked_users_colors = {}


### -----FUNCTIONS-----

def render_user(p, color):
    pygame.draw.circle(screen, (0,0,0), p, 5)
    pygame.draw.circle(screen, color, p, 4)

def increment(v1, v2, d):
    p = (v2[0]-v1[0], v2[1]-v1[1])
    if p == (0, 0):
        return v1
    s = d/sqrt(p[0]**2 + p[1]**2)
    p = (p[0]*s, p[1]*s)
    return (v1[0]+p[0], v1[1]+p[1])

# simple function to initialize data for a thread starter
def init_parent(thread, user_dict, color_dict):
    user_dict[str(thread.author)] = (
        random.uniform(-1*cx, cx),
        random.uniform(-1*cy, cy)
        )
    color_dict[str(thread.author)] = (
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255)
        )

def update_users(parent, comments, user_dict, comment_list, color_dict):
    for comment in comments:
        if comment.__class__.__name__ != 'MoreComments':
            if comment.fullname not in comment_list:
                comment_list.append(comment.fullname)
                if str(comment.author) not in user_dict:
                    # set random initial position
                    user_dict[str(comment.author)] = (
                        random.uniform(-1*cx, cx),
                        random.uniform(-1*cy, cy)
                        )
                    # set random color
                    color_dict[str(comment.author)] = (
                        random.randint(0,255),
                        random.randint(0,255),
                        random.randint(0,255)
                        )
                else:
                    # move user when new comment
                    user_dict[str(comment.author)] = increment(
                        user_dict[str(comment.author)],
                        user_dict[str(parent.author)],
                        inc
                        )
                    # draw user at new position
                    pos = user_dict[str(comment.author)]
                    pos_dest = (int(cx+pos[0]), int(cy+pos[1]))
                    render_user(
                        pos_dest,
                        color_dict[str(comment.author)]
                        )
            if len(comment.replies) > 0:
                update_users(comment, comment.replies, user_dict, comment_list, color_dict)

def update_threads(reddit, threads_dict, threads_queue, lim):
    top = reddit.get_front_page(limit=lim)
    for thread in top:
        if thread.id not in threads_queue:
            threads_queue.insert(0, thread.id)
            threads_dict[thread.id] = []
        else:
            del threads_queue[threads_queue.index(thread.id)]
            threads_queue.insert(0, thread.id)



### -----MAIN-----
            
r = praw.Reddit('Reddit test script -- amstocker.wordpress.com')
THREAD_COUNT = 50

while done == False:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                done = True

    screen.blit(eraser, (0,0))
    update_threads(r, tracked_threads, tracked_threads_queue, THREAD_COUNT)
    for thread_id in tracked_threads_queue[:THREAD_COUNT]:
        thread = r.get_submission(submission_id = thread_id)
        init_parent(thread, tracked_users, tracked_users_colors)
        update_users(
            thread,
            thread.comments,
            tracked_users,
            tracked_threads[thread_id],
            tracked_users_colors
            )
        print "updated @",time.time(),"//",thread_id,"//",len(tracked_threads[thread_id]),"comments"
    print "updated @",time.time(),"//",len(tracked_users),"users"
    pygame.display.flip()


pygame.quit()
        
