from flask import Flask, request
from multiprocessing import Process

import sue.logic as logic
from   sue.models import Message

import subprocess
import os

app = Flask(__name__)

def handler(buddyId, chatId, textBody, fileName):
    """Default handler that decides whether to contact Sue or not based on input
    """

    """buddyId is the number/email you contact Sue from. As I will need this
    entire string when I send the response back, I will keep it unaltered
    for now. Later, within Sue, a function can be used to get the raw
    data from it (number/email/etc) for use in db lookups for games/voting.

    Individual iMessage from an email:
        - B4C24F07-9A5C-4816-92BD-464AAE7C1A0A:sue@robertism.com
    Individual iMessage from phone:
        - B4C24F07-9A5C-4816-92BD-464AAE7C1A0A:+12223334444
    Group iMessage from phone:
        - 266A4860-0304-4B1E-AF1C-DE1145A7EC77:+12223334444

    Individual signal:
        - +12223334444
    Group signal:
        - +12223334444
    """

    """chatId is the uuid for the current group chat.

    Individual iMessage:
        - singleUser
    Group iMessage:
        - iMessage;+;chat123456789012345678

    Individual signal:
        - signal-singleUser
    Group signal:
        - signal-SNfoinsOINwnwfNWJ113rn==
    """
    if chatId != 'singleUser':
        if chatId[0:6] != 'signal':
            chatId = chatId.split('chat')[1]
    
    textBody = textBody.strip()

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
        textBody = textBody.split(' ', 1)
        textBody = textBody[1].strip() if len(textBody) > 1 else ''
    
    # create message object
    msg = Message(buddyId, chatId, textBody, fileName)

    # fetch the reply message
    sueReply = logic.process_reply(msg)

    # send the reply
    # add_to_response_queue(sueReply)

    if chatId == 'singleUser':
        response('individual', buddyId, 'good command')
    else:
        response('group', 'iMessage;+;chat'+chatId, 'good command')

def response(chatType, chatId, rmsg):
    command = ['osascript', 'direct.applescript', chatType, chatId, rmsg]
    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE)


@app.route('/', methods=['POST'])
def index():
    a = request.form['buddyId']
    b = request.form['chatId']
    c = request.form['textBody']
    d = request.form['fileName']

    # create process to handle this
    p = Process(target=handler, args=(a,b,c,d))
    p.start()
    
    # return '%s %s %s %s' % (a,b,c,d)
    return ''

if __name__ == "__main__":
    app.run(debug=True)