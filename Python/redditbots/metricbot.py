#!/usr/bin/python3
"""
This is a simple reddit bot that takes a temperature and converts it into its complementary format (celsius ->
fahrenheit, and vice versa). It only works when temperature unit is specified. As of 4/2/19, it won't respond to
comments that it has already responded to, even upon cold starts. Comment log is found in commentlog.txt.

Copyright © 2019 John Cooper Hopkin. All rights reserved. Contact the owner at coop.hopkin@gmail.com with any questions.
"""
import praw
import re
import os
import random
import socket
from datetime import datetime, timezone, timedelta


def celToFar(celsius):
    return round((float(celsius) * 9 / 5) + 32, 2)


def farToCel(faren):
    return round((float(faren) - 32) * 5 / 9, 2)

def get_instance():
    # create Reddit instance with info from praw.ini
    reddit = praw.Reddit('bot1')
    # Generate refresh token
    state = str(random.randint(0,65000))
    url = reddit.auth.url(duration="permanent", scopes=['identity'], state=state)
    print(f"Open this URL in your browser to to authenticate: {url}")

    client = receive_connection()
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    if state != params["state"]:
        send_message(
            client,
            f"State mismatch. Expected{state} Received: {params['state']}",
        )
        return 1
    elif "error" in params:
        send_message(client, params["error"])
        return 1
    
    refresh_token = reddit.auth.authorize(params["code"])
    send_message(client, f"Refresh token: {refresh_token}")
    with open("praw.ini", "a") as init:
        init.write("")
    return reddit

def receive_connection():
    """Wait for and then return a connected socket...
    
    Opens a TCP connection on port 8080 and waits for a single client
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client

def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()

def main():
    # get a refresh token
    with open("praw.ini", "r") as init:
        refresh_token_valid = False
        for line in init.readline():
            if "refresh_token" in line:
                expire_date = datetime.fromisoformat(init.readline().split("=")[1]) + timedelta(days=364)
                if datetime.now(timezone.utc) < expire_date:
                    refresh_token_valid = True

    if refresh_token_valid:
        reddit = praw.Reddit['bot1']
    else:
        reddit = get_instance()

    subreddit = reddit.subreddit("botprovingground")
    commentLog = open("commentlog.txt", 'w')

    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = list(filter(None, f.read().split("\n")))

    try:
        # precompile the regex string to apply to each comment
        passiveregex = re.compile("(-?\d+\.?(\d+)?) (degrees?) (\w+)")
        activeregex = re.compile("^(!convert).+?(-?\d+)\s?([FC]).+?(\sto\s)([FC]).*?")

        # finds each comment for the specified subreddit
        for comment in subreddit.stream.comments():

            # determines if the comment has a temperature to be converted
            m = passiveregex.search(comment.body, re.IGNORECASE)
            active = activeregex.search(comment.body. re.IGNORECASE)

            if comment in posts_replied_to:
                pass

            # if passive temperature string is found and "Conversion Bot says: " is not in the string,
            # convert the temperature
            elif m and not re.search("Conversion Bot says: ", comment.body, re.I):
                print(str(m[5]))
                commentLog.write(comment.body + '\n')
                posts_replied_to.append(comment)

                # Celsius to Fahrenheit
                if str(m[5]).lower()[0:2] == "c":
                    cel = m[1]
                    far = celToFar(cel)
                    conv_reply = "Conversion Bot says: " + str(m[1]) + " degrees Celsius is " + str(far) + \
                                 " degrees Fahrenheit!\n\nThis was your friendly neighborhood Conversion Bot!" + \
                                 "\n\nI am a bot. If something goes wrong, please PM my creator, Isitrelevantyet."
                    comment.reply(conv_reply)
                    commentLog.write('\t' + conv_reply + '\n')

                # Fahrenheit to Celsius
                elif m.toLower()[5] == "fahrenheit" or m[5] == "Fahrenheit":
                    faren = m[1]
                    cel = farToCel(faren)
                    conv_reply = "Conversion Bot says: " + str(m[1]) + " degrees Fahrenheit is " + str(cel) + \
                                 " degrees Celsius!\n\nThis was your friendly neighborhood Conversion Bot!" + \
                                 "\n\nI am a bot. If something goes wrong, please PM my creator, Isitrelevantyet."
                    comment.reply(conv_reply)
                    commentLog.write('REPLY:' + conv_reply + '\n')

            # If command word (!convert) is found, convert the temperature
            elif active:
                commentLog.write(comment.body + '\n')
                posts_replied_to.append(comment)

                # convert from celsius to fahrenheit
                if (active[2] == 'C' or active[2] == 'c') and (active[4] == 'F' or active[4] == 'f'):
                    cel = active[1]
                    far = celToFar(cel)
                    conv_reply = "Conversion Bot says: " + str(active[1]) + " degrees Celsius is " + str(far) + \
                                 " degrees Fahrenheit!\n\nThis was your friendly neighborhood Conversion Bot!" + \
                                 "\n\nI am a bot. If something goes wrong, please PM my creator, Isitrelevantyet."
                    comment.reply(conv_reply)
                    commentLog.write('\t' + conv_reply + '\n')

                # convert from fahrenheit to celsius
                elif (active[2] == 'F' or active[2] == 'f') and (active[4] == 'C' or active[4] == 'c'):
                    far = active[1]
                    cel = farToCel(far)
                    conv_reply = "Conversion Bot says: " + str(active[1]) + " degrees Fahrenheit is " + str(cel) + \
                                 " degrees Celsius!\n\nThis was your friendly neighborhood Conversion Bot!" + \
                                 "\n\nI am a bot. If something goes wrong, please PM my creator, Isitrelevantyet."
                    comment.reply(conv_reply)
                    commentLog.write('\t' + conv_reply + '\n')

    except (KeyboardInterrupt, SystemExit):
        commentLog.close()
        # print("in the except clause")
        with open('posts_replied_to.txt', 'a') as f:
            for item in posts_replied_to:
                f.write(str(item) + '\n')
        return 1


main()
