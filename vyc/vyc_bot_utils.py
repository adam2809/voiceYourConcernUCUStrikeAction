import requests
import json
from voiceYourConcern.settings import FB_KEY

def respond_to_msg(event):
    send_msg('jeb sie szmato',event['sender']['id'])


def send_msg(text,recipient):
    payload = {
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': recipient
        },
        'message': {
            'text': text
        }
    }

    return requests.post(
        url=f'https://graph.facebook.com/v6.0/me/messages?access_token={FB_KEY}',
        headers = {'content-type': 'application/json'},
        data=json.dumps(payload)
    )


# {"sender":{"id":"2884950064899015"},"recipient":{"id":"101417291453027"},"timestamp":1581791334914,"message":{"mid":"m_uK8w_1zHKsfpVUCAwOgL6v_X3Fz6RbZ5ad1rSq0hnhW8lu1YMebgheyVyh4xwlnk5meQNHVIWqOHXQ6S9bIFNA","text":"das"}}
