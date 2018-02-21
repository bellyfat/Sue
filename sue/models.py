class Message(object):
    def __init__(self, msgForm):
        self.buddyId, self.chatId, self.textBody, self.fileName = (None,) * 4

    @classmethod
    def _create_message(cls, msgForm):
        textBody = msgForm['textBody'].strip()

        # find the command we are being told to execute
        cls.command = textBody.split(' ', 1)[0].replace('!', '')

        # find the arguments for the command
        textBody = textBody.split(' ', 1)
        textBody = textBody[1].strip() if len(textBody) > 1 else ''

        # replace the unicode characters we changed in AppleScript back.
        cls.textBody = textBody.replace('¬¬¬', '$')

        cls.chatId = msgForm['chatId']

        # use our chatId to infer the type of group chat we're in.
        if cls.chatId == 'singleUser':
            cls.chatType = 'imessage-individual'
        elif 'iMessage;+;' in cls.chatId:
            cls.chatType = 'imessage-group'
        elif cls.chatId == 'signal-singleUser':
            cls.chatType = 'signal-individual'
        elif 'signal-' in cls.chatId:
            cls.chatType = 'signal-group'
        else:
            cls.chatType = '?'


        cls.buddyId = msgForm['buddyId']

        cls.fileName = msgForm['fileName'].replace('\n', '')

        return cls


# class Response(object):
#     def __init__(self, message):
