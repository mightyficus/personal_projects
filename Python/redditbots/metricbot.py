#!/usr/bin/python
"""
This is a simple reddit bot that takes a temperature and converts it into its complementary format (celsius ->
fahrenheit, and vice versa). It only works when temperature unit is specified. As of 4/2/19, it won't respond to
comments that it has already responded to, even upon cold starts. Comment log is found in commentlog.txt.

Copyright © 2019 John Cooper Hopkin. All rights reserved. Contact the owner at coop.hopkin@gmail.com with any questions.
"""
import praw
import re
import os


def celToFar(celsius):
    return round((float(celsius) * 9 / 5) + 32, 2)


def farToCel(faren):
    return round((float(faren) - 32) * 5 / 9, 2)


def main():
    reddit = praw.Reddit('bot1')
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
