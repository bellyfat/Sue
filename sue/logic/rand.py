import random

import flask
from sue.models import Message

app = flask.current_app
bp = flask.Blueprint('rand', __name__)

@bp.route('/random')
def sue_random():
    """!random <upper> <lower>"""
    msg = Message._create_message(flask.request.form)

    if not msg:
        return 'Error with message.'

    textBody = msg.textBody.lower()

    print(textBody)

    randRange = sorted(textBody.split(' '))
    if len(randRange) != 2:
        # can't have a range between 3 elements
        return sue_random.__doc__

    numberBased = set(map(lambda x: x.isdigit(), randRange))

    try:
        if numberBased == {True}:
            # 1 - 123
            randRange = [int(x) for x in randRange]
            randRange.sort()
            return str(random.randint(randRange[0],randRange[1]))
        elif numberBased == {False}:
            # a - z
            randRange = [ord(x) for x in randRange]
            randRange.sort()
            return str(chr(random.randint(randRange[0],randRange[1])))
        else:
            return str(random.random())
    except:
        return str(random.random())

@bp.route('/flip')
def flip():
    """!flip"""
    return random.choice(['heads','tails'])