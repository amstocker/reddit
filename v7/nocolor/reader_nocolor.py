import praw
import csv
from math import sqrt
import random
from time import localtime, strftime
from sys import argv

cx = 1024/2
cy = 768/2
inc = 3
INTERVALS = argv[1]

### -----DATA-----

tracked_threads = {}
tracked_threads_queue = []
tracked_users = {}

### -----FUNCTIONS-----

def increment(v1, v2, d):
    p = (v2[0]-v1[0], v2[1]-v1[1])
    if p == (0, 0):
        return v1
    s = d/sqrt(p[0]**2 + p[1]**2)
    p = (p[0]*s, p[1]*s)
    return (v1[0]+p[0], v1[1]+p[1])

def init_parent(thread, user_dict):
    author = str(thread.author)
    user_dict[author]= (
        random.uniform(-1*cx, cx),
        random.uniform(-1*cy, cy)
        )

def update_users(parent, comments, alist, user_dict, comment_list):
    for comment in comments:
        if comment.__class__.__name__ != 'MoreComments':
            if comment.fullname not in comment_list:
                comment_list.append(comment.fullname)
                author = str(comment.author)
                if author not in user_dict:
                    user_dict[author] = (
                        random.uniform(-1*cx, cx),
                        random.uniform(-1*cy, cy)
                        )
                else:
                    try:
                        npos = increment(
                            user_dict[author],
                            user_dict[str(parent.author)],
                            inc
                            )
                        user_dict[author] = npos
                        alist.append(npos)
                        
                    except KeyError as e:
                        args = e.args
                        print "===== USERNAME KEY ERROR"
                        print "=====", args[0], "user could not be found"
            if len(comment.replies) > 0:
                update_users(
                    comment,
                    comment.replies,
                    alist,
                    user_dict,
                    comment_list,
                    )

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
            
r = praw.Reddit('Reddit graphing script -- amstocker.wordpress.com')
f = open("actions.csv", "w")
w = csv.writer(f)
THREAD_COUNT = 50

CONT = True
while CONT == True:
    i = int(INTERVALS)
    while i > 0:
        actionlist = [strftime("%a, %d %b %Y %H:%M:%S", localtime())]
        connected = False
        while connected == False:
            try:
                update_threads(
                    r,
                    tracked_threads,
                    tracked_threads_queue,
                    THREAD_COUNT
                    )
                connected = True
            except:
                print "===== CONNECTION ERROR"
                time.sleep(30)
        for thread_id in tracked_threads_queue[:THREAD_COUNT]:
            connected = False
            while connected == False:
                try:
                    thread = r.get_submission(submission_id = thread_id)
                    init_parent(
                        thread,
                        actionlist,
                        tracked_users,
                        )
                    update_users(
                        thread,
                        thread.comments,
                        actionlist,
                        tracked_users,
                        tracked_threads[thread_id],
                        )
                    connected = True
                except:
                    print "===== CONNECTION ERROR"
                    time.sleep(30)

            stime = strftime("%a, %d %b %Y %H:%M:%S", localtime())
            print stime,"// updated",thread_id,"with",len(tracked_threads[thread_id]),"comments"
        w.writerow(actionlist)
        i -= 1
        stime = strftime("%a, %d %b %Y %H:%M:%S", localtime())
        print stime,"// updated",len(tracked_users),"users // approx.",i*0.036,"hours left" 

    valid = False
    while valid == False:
        try:
            n = int(raw_input("moar data? (0 to end) > "))
            if n == 0:
                CONT = False
                valid = True
            else:
                INTERVALS = n
                CONT = True
                valid = True
        except:
            print 'invalid entry'

f.close()
        







    

