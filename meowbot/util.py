from functools import wraps

from flask import Response, request, jsonify

from meowbot.appcontext import get_config


class ResponseType(object):

    EPHEMERAL = 'ephemeral'
    IN_CHANNEL = 'in_channel'


def get_response(type, text, attachments=None):
    response = {
        "response_type": type,
        "text": text,
    }
    if attachments:
        response["attachments"] = attachments

    return jsonify(response)


def get_verification_token():
    return get_config()['slack_verification_token']


def get_cat_api_key():
    return get_config()['cat_api_key']


def requires_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.get_json()['token'] != get_verification_token():
            return Response('Invalid token.', status=400)
        return f(*args, **kwargs)
    return decorated


def quote_user_id(user_id):
    return '<@{}>'.format(user_id)