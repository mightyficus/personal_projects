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


Functions adapted or copied from external sources noted in the function 
Copyright © 2023 Cooper Hopkin. All rights reserved. Contact the owner at coop.hopkin@gmail.com with any questions.
"""
import praw
import re
import random
import socket
from datetime import datetime, timezone, timedelta
import fileinput


def cel_to_far(celsius):
    """Convert Celsius to Fahrenheit"""

    return round((float(celsius) * 9 / 5) + 32, 2)


def far_to_cel(faren):
    """Convert Fahrenheit to Celsius"""

    return round((float(faren) - 32) * 5 / 9, 2)

def get_token():
    """ Create a temporary Reddit instance to retrieve a refresh token

        Function adapted from the main function here:
        https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html#refresh-token
    """

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
    """Wait for and then return a connected socket.

        Opens a TCP connection on port 8080, and waits for a single client.
        Copied from receive_connection() function here:
        https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html#refresh-token
    """

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client

def send_message(client, message):
    """Send message to client and close the connection.

        Copied from send_message() function here:
        https://praw.readthedocs.io/en/stable/tutorials/refresh_token.html#refresh-token
    """

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
        # the recursion from restarting process after successful bot process ends
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

    # precompile the regex string to apply to each comment
    passiveregex = re.compile("(?P<temp>-?\d+\.?(\d+)?) ?((?:degrees?)|°)? ?(?P<pre_unit>[FC])", re.IGNORECASE)
    activeregex = re.compile("^(!convert).+?(?P<temp>-?\d+)\s?((?:degrees?)|°)?\s?(?P<pre_unit>[FC])(\sto\s)([FC])", re.IGNORECASE)


    # finds each comment for the specified subreddit
    for comment in subreddit.stream.comments(skip_existing=True):
        try:
        # We shouldn't respond to the bot comments, otherwise we get an infinite loop
            if comment.author != 'conversion_bot_test':

                # determines if the comment has a temperature to be converted
                passive = passiveregex.search(comment.body)
                active = activeregex.search(comment.body,)
                # If command word (!convert) is found, convert temp
                if active:
                    # DEBUG: Print comment that's being responded to
                    print(f"Active response: {str(comment.body)}")

                    # Set the temperature we'll be converting
                    pre_temp = float(active['temp'])

                    # Set the pre/post unit to longhand unit name and convert
                    # temperature according to specified pre-conversion unit
                    if active['pre_unit'][0].lower() == 'c':
                        pre_unit = 'Celsius'
                        post_unit = 'Fahrenheit'
                        post_temp = cel_to_far(pre_temp)
                    elif active['pre_unit'][0].lower() == 'c':
                        pre_unit = 'Fahrenheit'
                        post_unit = 'Celsius'
                        post_temp = far_to_cel(pre_temp)
                    # If the unit we are converting from is missing, assume a bad 
                    # comment and just start again with next comment
                    # If regex works, this should never trigger
                    else:
                        continue

                # if passive temperature string is found convert the temperature
                elif passive:
                    # DEBUG: Print comment being responded to
                    print(f"Passive Response: {str(comment.body)}")

                    # Set the temperature we'll be converting
                    pre_temp = float(passive['temp'])

                    # Set the pre/post unit to longhand unit name and convert
                    # temperature according to specified pre-conversion unit
                    if passive['pre_unit'][0].lower() == 'c':
                        pre_unit = 'Celsius'
                        post_unit = 'Fahrenheit'
                        post_temp = cel_to_far(pre_temp)
                    elif passive['pre_unit'][0].lower() == 'f':
                        pre_unit = 'Fahrenheit'
                        post_unit = 'Celsius'
                        post_temp = far_to_cel(pre_temp)
                    # If the unit we are converting from is missing, assume a bad 
                    # comment and just start again with next comment
                    # If regex works, this should never trigger
                    else:
                        continue

                    """if str(m[5]).lower()[0] == "c":
                        before_conv = m[1]
                        after_conv = cel_to_far(cel)
                        conv_reply = "Conversion Bot says: " + str(m[1]) + " degrees Celsius is " + str(far) + \
                                        " degrees Fahrenheit. This was your friendly neighborhood Conversion Bot!" + \
                                        "\n\n^(I am a bot. If something goes wrong, please PM my creator, Isitrelevantyet.)"
                        comment.reply(conv_reply)

                    # Fahrenheit to Celsius
                    elif str(m[5]).toLower()[0:2] == "f":
                        before_conv = m[1]
                        after_conv = far_to_cel(faren)
                        conv_reply = "Conversion Bot says: " + str(m[1]) + " degrees Fahrenheit is " + str(cel) + \
                                        " degrees Celsius!\n\nThis was your friendly neighborhood Conversion Bot!" + \
                                        "\n\nI am a bot. If something goes wrong, please PM my creator, Isitrelevantyet."
                        comment.reply(conv_reply)"""
                    
                # If the comment doesn't contain units to convert, move on to next comment
                else:
                    print(f"No Response: {str(comment.body)}")
                    continue
                
                conv_reply = "Conversion Bot says: " + str(pre_temp) + " degrees "+ pre_unit + " is " + str(post_temp) + \
                                        " degrees "+ post_unit +". This was your friendly neighborhood Conversion Bot!" + \
                                        "\n\n^(I am a bot. If something goes wrong, please PM my creator, Isitrelevantyet.)"

                comment.reply(conv_reply)
            else: 
                continue
        except KeyboardInterrupt:
            print("Exiting!")
            return 0
        except:
            print("System Error! Exiting...")
            return 1
            
    return 0

if __name__ == "__main__":
    main()
