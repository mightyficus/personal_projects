#!/usr/bin/python3
"""
This is a reddit bot for temperature conversion between Celsius and Fahrenheit

The praw.ini file should look like this:

    [DEFAULT]
    # A boolean to indicate whether or not to check for package updates.
    check_for_updates=True

    # Object to kind mappings
    comment_kind=t1_
    message_kind=t4_
    redditor_kind=t2_
    submission_kind=t3_
    subreddit_kind=t5_

    # The URL prefix for OAuth-related requests.
    oauth_url=https://oauth.reddit.com

    # The URL prefix for regular requests.
    reddit_url=https://www.reddit.com

    # The URL prefix for short URLs.
    short_url=https://redd.it

    [bot1]
    client_id=<generated client id>
    client_secret=<generated client secret
    redirect_uri=http://localhost:8080
    # If a refresh value hasn't been generated yet, use these values as dummies.
    # When the bot is validated for the first time, these values should populate.
    refresh_token=fake_value

    bot_name=ConversionBot
    bot_version=0.0.1
    bot_author=isitrelevantyet
    user_agent=praw-script:%(bot_name)s:v%(bot_version)s (by u/%(bot_author)s)

Copyright © 2023 Cooper Hopkin. All rights reserved. Contact the owner at coop.hopkin@gmail.com with any questions.
"""
import praw
import re
import os
import random
import socket
from datetime import datetime, timezone, timedelta
import fileinput


def cel_to_far(celsius):
    return round((float(celsius) * 9 / 5) + 32, 2)


def far_to_cel(faren):
    return round((float(faren) - 32) * 5 / 9, 2)

def get_token():
    # Create a temporary instance to retrieve a refresh token
    reddit_temp = praw.Reddit('bot1')

    # Generate an authorization token
    state = str(random.randint(0,65000))
    url = reddit_temp.auth.url(duration="permanent", scopes=['account','flair','history','identity','livemanage','read','save','submit'], state=state)
    print(f"Open this URL in your browser to to authenticate: {url}")

    # Set up a simple redirect URI socket to retrieve the authorization token
    client = receive_connection()

    # Parse the HTTP response
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    # We somehow receive a response with the wrong state. Discard and exit 
    if state != params["state"]:
        send_message(
            client,
            f"State mismatch. Expected{state} Received: {params['state']}",
        )
        return 1
    # Error happened with authorization request. Print error and exit
    elif "error" in params:
        send_message(client, params["error"])
        return 1
    
    # Retreive a refresh token by authorizing the instance with the authorization token
    refresh_token = reddit_temp.auth.authorize(params["code"])

    # Print refresh token to the command line, send it to the redirect url, and return it
    print(refresh_token)
    send_message(client, f"Refresh token: {refresh_token}")
    return refresh_token

        
def receive_connection():
    """
    Wait for and then return a connected socket.
    Opens a TCP connection on port 8080, and waits for a single client.
    """

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client

def send_message(client, message):
    # Send message to client and close the connection.
    print(message)
    client.send(f"HTTP/1.1 200 OK\r\n\r\n{message}".encode("utf-8"))
    client.close()


def main():  
    # check if praw.ini already has a refresh token
    with open("praw.ini", "r") as init:
        for line in init:
            if "refresh_token" in line:
                # retrieve refresh token from praw.ini file (praw.Reddit will 
                # not automatically retrieve token from file during ititialization)
                refresh_token = line.split("=")[1].strip()
                break
    
    # Try to create a praw.Reddit instance
    reddit = praw.Reddit('bot1', refresh_token=refresh_token)

    # If reddit.auth.scopes() returns the scopes, the refresh token was valid. If it 
    # doesn't, the refresh token is invalid (bad token or permissions were revoked) and a 
    # new one needs to be generated
    try:
        print(f"Scopes enabled:{reddit.auth.scopes()}")
    except:
        print("Invalid refresh token!")
        # Request a new refresh token
        refresh_token = get_token()
        # Replace old token with new token in praw.ini
        with fileinput.input("praw.ini", inplace=1) as init:
            for line in init:
                if "refresh_token" in line:
                    line = line.replace(line, f"refresh_token={refresh_token}")
                    print(line)
                else:
                    print(line, end='')
        # try again from the beginning using recursion. Return afterwards to avoid 
        # recursing restarting process after successful bot process ends
        main()
        return 0


    subreddit = reddit.subreddit("botprovingground")
    
    # precompile the regex string to apply to each comment
    passiveregex = re.compile("(-?\d+\.?(\d+)?) (degrees?) (\w+)")
    activeregex = re.compile("^(!convert).+?(-?\d+)\s?([FC]).+?(\sto\s)([FC]).*?")

    # for comment in subreddit.stream.comments(skip_existing=True):
    #     m = passiveregex.search(comment.body, re.IGNORECASE)
    #     active = activeregex.search(comment.body. re.IGNORECASE)

    #     if comment.author == reddit.user.me():
    #         pass

    """try:
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
"""

if __name__ == "__main__":
    main()
