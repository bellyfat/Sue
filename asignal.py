# -*- coding: utf-8 -*-
import sys
from pprint import pprint

def a_signal(sender, groupId, inputText, fileName):
    inputText = unicode(inputText).encode('utf-8')

    try:
        """ Note that:
        buddyId, chatId, inputText, fileName becomes
        sender, groupId, textBody, fileName. """

        if groupId != 'singleUser':
            if groupId[0:6] != 'signal':
                groupId = groupId.split('chat')[1]

        textBody = inputText
        fileName = fileName.replace('\n','')
    except:
        print('>.<')
        exit()

    if len(textBody.strip()) == 0:
        # no text. Just a space.
        exit()

    if textBody.strip()[0] is not '!':
        # we aren't being called upon to do anything. Ignore the message.
        exit()
    else:
        # find the command we are being told to do, and execute it.
        # try:
        textBody = textBody.strip().replace('¬¬¬','"')
        command = textBody.split(' ',1)[0].replace('!','')
        if not command:
            exit()
        textBody = textBody.split(command,1)[1].strip()
        # except:
        #     print('Error parsing: ==='+textBody+'===')
        #     exit()

        from b import sue
        sue(sender, groupId, command.lower(), textBody, fileName)
