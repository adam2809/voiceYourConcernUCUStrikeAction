import requests
import json
from voiceYourConcern.settings import FB_KEY

GET_STARTED_RESPONSE_MSGS = [
    'As students we want to support our lectures during the UCU strike action!',
    'Learn more at https://www.ucu.org.uk/strikeforuss.',
]

fb_api_url = f'https://graph.facebook.com/v6.0/me/messages?access_token={FB_KEY}'


def handle_message(req_body):
    print(req_body)

    if req_body['object'] == 'page':
        for entry in req_body['entry']:
            for event in entry['messaging']:
                dispatch_event(event)


def dispatch_event(event):
    if 'postback' in event:
        dispatch_postback_event(event)
        return

    if 'message' in event and event['message']['text']:
        respond_to_msg(event)


def dispatch_postback_event(event):
    tmp = event['postback']['payload'].split('/')
    q = tmp[0]
    a = tmp[1] if len(tmp) > 1 else None

    if q == 'get_started':
        respond_to_get_started(event)
        return

    if q == 'send_email':
        if a == 'yes':
            start_send_email_convo(event['sender']['id'])
        else:
            send_no_email_response(event['sender']['id'])


def respond_to_msg(event):
    send_msg('One of the page admins will respond shortly',event['sender']['id'])


def respond_to_get_started(event):
    for msg in GET_STARTED_RESPONSE_MSGS:
        send_msg(msg,event['sender']['id'])

    show_send_email_postback_buttons(event['sender']['id'])


def start_send_email_convo(recipient_id):
    send_msg('pogadajmy o tym mejlu',recipient_id)


def send_no_email_response(recipient_id):
    send_msg('jak nie to nie',recipient_id)


def show_send_email_postback_buttons(recipient_id):
    payload = {
        "recipient":{
            "id":recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Send angry email?",
                    "buttons":[
                        {
                            "type":"postback",
                            "title":"Yes",
                            "payload":"send_email/yes"
                        },
                        {
                            "type":"postback",
                            "title":"No",
                            "payload":"send_email/no"
                        },
                    ]
                }
            }
        }
    }

    return requests.post(
        url=fb_api_url,
        headers = {'content-type': 'application/json'},
        data=json.dumps(payload)
    )


def send_msg(text,recipient_id):
    payload = {
        'messaging_type': 'RESPONSE',
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': text
        }
    }

    return requests.post(
        url=fb_api_url,
        headers = {'content-type': 'application/json'},
        data=json.dumps(payload)
    )
