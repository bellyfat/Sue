"""
Currently, when running things on my home server, I have to remote-desktop in
and copy-paste my code (because I don't want to pollute the repo with a bunch of
commits). This will be a way for me to run my code without having to worry about
that stuff.
"""

import requests

while True:
    print('================================================================================')
    inputStr = input('YOU : ')
    payload = {
        'chatId' : 'debug',
        'textBody' : inputStr,
        'buddyId' : '',
        'fileName' : ''
    }
    r = requests.get('http://localhost:5000/', data=payload)
    print('SUE : \n{0}'.format(r.content.decode('utf8')))