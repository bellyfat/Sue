import subprocess
import sys
import os
from pprint import pprint
from abc import ABC, abstractmethod
from urllib.parse import quote

from sue.utils import reduce_output, secure_string

class Message(object):
    def __init__(self, msgForm):
        self.buddyId, self.chatId, self.textBody, self.fileName = (None,) * 4

    @classmethod
    def _create_message(cls, msgForm):
        """Used to initialize a method if it exists, or return null if it is not
        a message that sue will be using to 

        Parameters
        ----------
            msgForm : flask.request.form
        """
        textBody = msgForm['textBody'].strip()

        # find the command we are being told to execute
        cls.command = textBody.split(' ', 1)[0].replace('!', '').lower()

        # find the arguments for the command
        textBody = textBody.split(' ', 1)
        textBody = textBody[1].strip() if len(textBody) > 1 else ''

        # replace the unicode characters we changed in AppleScript back.
        cls.textBody = textBody.replace('¬¬¬', '$').replace('ƒƒƒ', '+')

        cls.chatId = msgForm['chatId'].replace('ƒƒƒ', '+')

        # use our chatId to infer the type of group chat we're in.
        if cls.chatId == 'singleUser':
            cls.chatType = 'imessage-individual'
        elif 'iMessage;+;' in cls.chatId:
            cls.chatType = 'imessage-group'
        elif cls.chatId == 'signal-singleUser':
            cls.chatType = 'signal-individual'
        elif 'signal-' in cls.chatId:
            cls.chatType = 'signal-group'
        elif cls.chatId == 'debug':
            cls.chatType = 'debug'
        else:
            cls.chatType = '?'

        cls.buddyId = msgForm['buddyId'].replace('ƒƒƒ', '+')

        # specify iMessage or signal as the platform
        if 'imessage' in cls.chatType:
            cls.platform = 'imessage'
        elif 'signal' in cls.chatType:
            cls.platform = 'signal'
        elif cls.chatType == 'debug':
            cls.platform = 'debug'
        else:
            cls.platform = '?'

        # extract the phone number of the sender
        if cls.platform is 'imessage':
            sender = cls.buddyId.split(':',1)
            if len(sender) > 1:
                cls.sender = sender[1]
            else:
                print('There was an error extracting the sender info.')
                cls.sender = cls.buddyId
        elif cls.platform is 'signal':
            cls.sender = cls.buddyId
        else:
            cls.sender = '?'

        cls.fileName = msgForm['fileName'].replace('\n', '')

        return cls

class Response(ABC):
    """Base class used for sending Sue's response back to the user.
    The classes associated with connecting to iMessage and Signal both inherit
    from this. It's also used by the debug client, `debug.py`.

    Parameters
    ----------
    origin_message : Message
        The flask.request.form we have casted into a message. Contains info
          as to which group to send our response back to.
    sue_response : str
        All of our functions either return a string, or a list of strings that
          is then reduced (x+'\n'+y) back into a single string. This response
          string is what is sent back to the user.
    attachment : str
        The file path of any attachment we wish to send. We currently only
          support sending back files in iMessage. I plan on setting the message
          to an empty string ("") when there is an attachment, unless I find a
          scenario where I want to send an image and a string back.
    """
    def __init__(self, origin_message, sue_response, attachment=None):
        self.origin_message = origin_message
        self.sue_response = sue_response
        self.attachment = attachment

        if origin_message.buddyId == 'debug':
            print('### DEBUG ###')
            pprint(self.sue_response)
        else:
            self.send()

    @abstractmethod
    def send(self, origin_message, sue_response):
        pass

class IMessageResponse(Response):
    """Used to send Sue's respose back to groups/individuals on iMessage.
    Called when msg.platform is 'imessage'.
    
    See `Response` class for more info on parameters.
    """

    def __init__(self, origin_message, sue_response, attachment=None):
        # super() sets attachment
        super().__init__(origin_message, sue_response, attachment=attachment)
    
    def send():
        FNULL = open(os.devnull, 'wb')
        
        command = ["osascript",
                   "direct.applescript",
                   secure_string(self.origin_message.chatId),
                   secure_string(self.origin_message.buddyId),
                   secure_string(self.sue_response)]
        
        if self.attachment:
            f = secure_string(self.attachment)
            command.extend(['file', f])
        else:
            command.append('msg')
        
        print(command)

        print('Sending response.')
        subprocess.Popen(command, stdout=FNULL)

        FNULL.flush()
        FNULL.close()

class SignalResponse(Response):
    def __init__(self, origin_message, sue_response, attachment=None):
        super().__init__(origin_message, sue_response, attachment=attachment)
    
    def send():
        raise NotImplementedError("Still thinking about how GET -> Response...")

class DirectResponse():
    def __init__(self, recipient, sue_response):
        self.send_to_queue(recipient, sue_response)
    
    def send_to_queue(self, recipient, sue_response):
        VIPs = {
            'robert' : ('+12107485865', 'phone'),
            'james'  : ('+12108603312', 'phone')
        }

         # detect if recipient is phoneNumber or iMessage email
        if '+' in recipient:
            method = 'phone'
        elif '@' in recipient:
            method = 'email'
        else:
            recipient, method = VIPs.get(recipient, (None, None))

        if not recipient:
            # still can't find it.
            print('Error matching recipient.')
            return

        FNULL = open(os.devnull, 'wb')
        
        # TODO: rename the applescript files to actually reflect what they do.
        command = ["osascript",
                   "actuallydirect.applescript",
                   secure_string(recipient),
                   secure_string(method),
                   secure_string(sue_response)]
        
        print(command)
        subprocess.Popen(command, stdout=FNULL)

        FNULL.flush()
        FNULL.close()
