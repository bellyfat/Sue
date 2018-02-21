"""
Welcome to the re-design for Sue. I wanted something that had minimalist hook
declarations with decorators (similar to Flask's routing), and done in a way
that was async, clean, and able to be easily modified by the community.

Notes that I've made along the way:
- All print() functions will be substituted for logging funcs at a later date.
- 
"""

import subprocess
import sys
import os

FNULL = open(os.devnull, 'wb')

def send_to_queue(buddyId, chatId, textBody, fileName):
    command = ["osascript","display.applescript"]
    msg = textBody
    command.extend([str(len(sys.argv))])
    
    subprocess.Popen(command, stdout=FNULL)

if __name__ == "__main__":
    if len(sys.argv != 5):
        print('Wrong number of inputs.')
        exit(1)

    """buddyId is the number/email you contact Sue from. As I will need this
    entire string when I send the response back, I will keep it unaltered
    for now. Later, within Sue, a function can be used to get the raw
    data from it (number/email/etc) for use in db lookups for games/voting.

    Individual imessage from an email:
        - B4C24F07-9A5C-4816-92BD-464AAE7C1A0A:sue@robertism.com
    Individual imessage from phone:
        - B4C24F07-9A5C-4816-92BD-464AAE7C1A0A:+12107485865
    Group imessage from phone:
        - 266A4860-0304-4B1E-AF1C-DE1145A7EC77:+12107485865
    
    Individual signal:
        - +12107485865
    Group signal:
        - +12107485865
    """
    buddyId = sys.argv[1]

    # indiv imessage:
    #     "singleUser"
    # group imessage:
    #     "iMessage;+;chat425760385495712678"
    """chatId is the uuid for the current group chat.

    Individual imessage:
        - singleUser
    Group imessage:
        - iMessage;+;chat425760385495712678
    
    Individual signal:
        - signal-singleUser
    Group signal:
        - signal-YGGqUfw8wPY7QQi1CCg4tA==
    """
    chatId = sys.argv[2]
    if chatId != 'singleUser':
        if chatId[0:6] != 'signal':
            chatId = chatId.split('chat')[1]

    textBody = sys.argv[3].strip()

    # noFile
    fileName = sys.argv[4]
    fileName = fileName.replace('\n','')

    # parse message for relevant information
    if len(textBody) == 0:
        # no text, just a space.
        exit(0)
    
    if textBody[0] is not '!':
        # we aren't being called upon to do anything. Ignore the message.
        exit(0)
    else:
        # find the command we are being told to execute, and execute it.
        command = textBody.split(' ', 1)[0].replace('!','')
        if not command:
            # it was just exclamation marks
            exit(0)
        textBody = textBody.split(' ',1)
        textBody = textBody[1].strip() if len(textBody) > 1 else ''

    # send information to function handler
    send_to_queue(buddyId, chatId, textBody, fileName)