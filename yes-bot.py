import praw
import config
import time

visited_sub_list = []
new_sub_list = []

visited_comment_list = []
new_comment_list = []

def build_sub_list():
    visited = open("submissions.txt", "r")
    for line in visited:
        visited_sub_list.append(line[:-1])
    visited.close()

def build_comment_list():
    read = open("comments.txt","r")
    for line in read:
        visited_comment_list.append(line[:-1])
    read.close()

def bot_login():
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         password=config.password,
                         user_agent=config.user_agent,
                         username=config.username)
    #print (reddit.user.me(), "logged in")
    reddit.read_only = False
    return reddit

def read_submissions(sub, r):
    subreddit = r.subreddit(sub)
    for submission in subreddit.hot(limit=25):
        print (submission.id)
        if str(submission.id) not in visited_sub_list:
            # print ("Title: " + submission.title)
            # print("Text: " + submission.selftext)
            # print("---------------------------------------- \n")
            read_comments(submission, r)
            new_sub_list.append(submission.id)
            visited_sub_list.append(submission.id)

def read_comments(submission,r):
    for comment in submission.comments.list():
        if str(comment.id) not in visited_comment_list:
            if (("DO" in comment.body.upper() or "DOES" in comment.body.upper() or "DID" in comment.body.upper()) and ("OR" in comment.body.upper())) or ("OR?" in comment.body.upper()):          
                print "Replying to comment..."
                comment.reply("Yes. \n\n------------------- \nBeep Boop. I am a bot. I reply with a yes just like a redditor would. I'm going to help AI take over the world")
            if ("NICE JOB" in comment.body.upper() or "GOOD WORK" in comment.body.upper() or "BRILLIANT" in comment.body.upper() or "GOOD JOB" in comment.body.upper()):
                print "Replying to comment..."
                comment.reply("Thanks! \n\n------------------- \nBeep Boop. I am a bot. I reply with a yes just like a redditor would. I'm going to help AI take over the world")
            new_comment_list.append(comment.id)
            write_to_visited(new_sub_list, new_comment_list)
            visited_comment_list.append(comment.id)
        

            


def write_to_visited(sub_v, sub_c):
    visited_sub = open("submissions.txt","a")
    visited_com = open("comments.txt", "a")
    print "Writing to", visited_sub.name,"and", visited_com.name
    for num in sub_v:
        visited_sub.write(num + "\n")
    visited_sub.close()
    for com in sub_c:
        visited_com.write(com + "\n")
    visited_com.close()
    #sub_v = sub_c = []


r = bot_login()


while True:
    build_sub_list()
    build_comment_list()
    read_submissions("pavlovedoncaffeine", r)
    


#sub = raw_input("Enter the subreddit you'd like to parse: ")
#read_submissions(sub, r)
