import requests
import json
from voiceYourConcern.settings import FB_KEY
from vyc.models import QA

GET_STARTED_RESPONSE_MSGS = [
    'As students we want to support our lectures during the UCU strike action!',
    'Learn more at https://www.ucu.org.uk/strikeforuss.',
]

fb_api_url = f'https://graph.facebook.com/v6.0/me/messages?access_token={FB_KEY}'




def handle_message(req_body):
    if req_body['object'] == 'page':
        for entry in req_body['entry']:
            for event in entry['messaging']:
                dispatch_event(event)


def dispatch_event(event):
    if 'postback' in event:
        dispatch_postback_event(event)
        return


def dispatch_postback_event(event):
    q,a = event['postback']['payload'].split('/')

    if not q == 'get_started':
        QA(
            u_id=event['sender']['id'],
            question=q,
            anwser=a,
        ).save()

    qa_mapping = {
        'get_started':{
            'none' : get_started_response
        },
        'send_email':{
            'yes' : send_email_yes_response,
            'no' : send_email_no_response,
        },
        'use_template':{
            'yes' : use_template_yes_response,
            'no' : use_template_no_response,
        },
        'confirm_input_content':{
            'ok' : confirm_input_content_ok_response,
            'discard' : confirm_input_content_discard_response,
        },
        'confirm_send_email':{
            'ok' : confirm_send_email_ok_response,
            'discard' : confirm_send_email_discard_response,
        },
    }
    qa_mapping[q][a](event['sender']['id'])


def get_started_response(recipient_id):
    for msg in GET_STARTED_RESPONSE_MSGS:
        send_msg(msg,recipient_id)

    show_send_email_postback_buttons(recipient_id)


def show_send_email_postback_buttons(recipient_id):
    text = "Send angry email?"
    buttons = [
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
    show_postback_buttons(recipient_id,text,buttons)


def send_email_yes_response(recipient_id):
    text = 'Would you like to use an email templete recommended by UCU?'
    buttons = [
        {
            "type":"postback",
            "title":"Yes",
            "payload":"use_template/yes"
        },
        {
            "type":"postback",
            "title":"No",
            "payload":"use_template/no"
        },
    ]
    show_postback_buttons(recipient_id,text,buttons)


def send_email_no_response(recipient_id):
    send_msg('jak nie mejl to nie',recipient_id)


def use_template_yes_response(recipient_id):
    send_msg('Gimmie your email',recipient_id)


def use_template_no_response(recipient_id):
    send_msg('Gimmie your content',recipient_id)


def confirm_input_content_ok_response(recipient_id):
    send_msg('Content accepted',recipient_id)


def confirm_input_content_discard_response(recipient_id):
    send_msg('Content thrown out',recipient_id)


def confirm_send_email_ok_response(recipient_id):
    send_msg('email sent',recipient_id)


def confirm_send_email_discard_response(recipient_id):
    send_msg('email discarded',recipient_id)



def show_postback_buttons(recipient_id,text,buttons):
    payload = {
        "recipient":{
            "id":recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":text,
                    "buttons":buttons
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
