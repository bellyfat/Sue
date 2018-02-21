import flask

from sue.models import Message

app = flask.current_app
bp = flask.Blueprint('main', __name__)

def check_command(msgForm):
    """
    Checks to make sure:
        1. we are actually being called to execute a command
        2. we have all the necessary parameters to execute it
    :param msgForm: a dictionary representing our GET request.
    :return: String of the command. Empty string if none exists.
    """

    # check to see the message contains all the information we require.
    required_keys = {'buddyId', 'chatId', 'textBody', 'fileName'}
    if len(set(msgForm.keys()) & required_keys) != 4:
        return ''

    textBody = msgForm['textBody'].strip()

    if len(textBody) == 0:
        # no text, just a space.
        return ''

    if textBody[0] is not '!':
        # we aren't being called upon to do anything. Ignore the message.
        return ''
    else:
        # find the command we are being told to execute, and execute it.
        command = textBody.split(' ', 1)[0].replace('!', '')
        if not command:
            # it was just exclamation marks
            return ''

    return command

@bp.route('/')
def process_reply():
    command = check_command(flask.request.form)

    if not command:
        return ''

    return flask.redirect(command, code=307)

    # return flask.redirect(msg.command, code=307)
    # get reply back from Sue
    # response = Reponse(msg)
    # send_reply(response)