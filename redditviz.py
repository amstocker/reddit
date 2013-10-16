import pygame
import praw
import time
from pprint import pprint


r = praw.Reddit('Reddit graphing testing by /u/sleepyams -- amstocker.wordpress.com')
# tracked thread
thread = r.get_submission(submission_id = "1oixi8")
# tracked users ==> { 'user' : [pos0, pos1, pos2, ...] }
tracked = {}

comments = thread.comments

def recursive_print(replies):
    for reply in replies:
        print reply.author
        if len(reply._replies) > 0:
            recursive_print(reply._replies)

recursive_print(thread._comments)
        
