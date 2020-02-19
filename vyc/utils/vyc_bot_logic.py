import requests
import json
import re

from voiceYourConcern.settings import FB_KEY
from vyc.models import QA,State

from vyc.utils.vyc_bot_responses import MESSAGES,POSTBACKS,UCU_TEMPLATE_CONTENT,UCU_TEMPLATE_HEADER,UCU_TEMPLATE_FOOTER,VC_EMAIL_ADDRESS
from vyc.utils.email import send_email

GET_STARTED_RESPONSE_MSGS = [
    'As students we want to support our lectures during the UCU strike action!',
    'Learn more at https://www.ucu.org.uk/strikeforuss.',
]

fb_api_url = f'https://graph.facebook.com/v6.0/me/messages?access_token={FB_KEY}'

EMAIL_ADDRESS_REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def handle_message(req_body):
    if req_body['object'] == 'page':
        for entry in req_body['entry']:
            for event in entry['messaging']:
                print(event)
                dispatch_event(event)


def dispatch_event(event):
    if 'postback' in event:
        dispatch_postback_event(event)
        return

    if 'message' in event:
        curr_state = State.objects.filter(u_id=event['sender']['id'])
        if not curr_state.exists():
            return

        if curr_state[0].state == 'email_wait':
            input_email_response(event['sender']['id'],event['message']['text'])
            return

        if curr_state[0].state == 'content_wait':
            input_content_response(event['sender']['id'],event['message']['text'])
            return

        if curr_state[0].state == 'name_wait':
            input_name_response(event['sender']['id'],event['message']['text'])
            return



def dispatch_postback_event(event):
    q,a = event['postback']['payload'].split('/')

    if not q == 'get_started':
        set_QA(event['sender']['id'],q,a)

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
            'discard' : discard_flow,
        },
        'confirm_send_email':{
            'ok' : confirm_send_email_ok_response,
            'discard' : discard_flow,
        },
        'cancel_input':{
            'none' : discard_flow,
        }

    }
    qa_mapping[q][a](event['sender']['id'])


def get_started_response(recipient_id):
    send_msg_list(MESSAGES['get_started'],recipient_id)
    show_url_buttons(recipient_id)
    show_postback_buttons(recipient_id,**POSTBACKS['get_started'])
    send_msg("If you have any questions don't hasitatate to ask and one of the page administrators should get back you you soon.")




def send_email_yes_response(recipient_id):
    show_postback_buttons(recipient_id,**POSTBACKS['send_email_yes'])


def send_email_no_response(recipient_id):
    clear_session(recipient_id)
    send_msg_list(MESSAGES['send_email_no'],recipient_id)


def use_template_yes_response(recipient_id):
    set_QA(recipient_id,'use_template','yes')
    set_state(recipient_id,'email_wait')
    show_postback_buttons(recipient_id,**POSTBACKS['email_input_prompt'])


def use_template_no_response(recipient_id):
    set_QA(recipient_id,'use_template','no')
    set_state(recipient_id,'content_wait')
    send_msg_list(MESSAGES['use_template_no'],recipient_id)


def input_content_response(recipient_id,anwser):
    set_QA(recipient_id,'get_content',anwser)
    set_state(recipient_id,'')
    show_postback_buttons(recipient_id,**POSTBACKS['input_content'])


def confirm_input_content_ok_response(recipient_id):
    set_state(recipient_id,'email_wait')
    show_postback_buttons(recipient_id,**POSTBACKS['email_input_prompt'])


def discard_flow(recipient_id):
    clear_session(recipient_id)
    send_msg_list(MESSAGES['discard_flow'],recipient_id)


def input_email_response(recipient_id,anwser):
    if not is_address_valid(anwser.strip()):
        show_postback_buttons(recipient_id,**POSTBACKS['invalid_email'])
        return

    set_QA(recipient_id,'get_email',anwser)
    set_state(recipient_id,'name_wait')
    show_postback_buttons(recipient_id,**POSTBACKS['input_email'])


def is_address_valid(email):
    return bool(re.search(EMAIL_ADDRESS_REGEX,email))


def input_name_response(recipient_id,anwser):
    set_QA(recipient_id,'get_name',anwser)
    set_state(recipient_id,'')
    show_postback_buttons(recipient_id,**POSTBACKS['input_name'])


def confirm_send_email_ok_response(recipient_id):
    clear_state(recipient_id)

    use_template_anws = QA.objects.all().filter(
        u_id=recipient_id,
        question='use_template'
    )
    get_content_anws = QA.objects.all().filter(
        u_id=recipient_id,
        question='get_content'
    )
    get_email_anws = QA.objects.all().filter(
        u_id=recipient_id,
        question='get_email'
    )
    get_name_anws = QA.objects.all().filter(
        u_id=recipient_id,
        question='get_name'
    )

    footer_with_name = UCU_TEMPLATE_FOOTER % get_name_anws[0].anwser
    msg=f'{UCU_TEMPLATE_HEADER}%s{footer_with_name}'

    if use_template_anws[0].anwser == 'yes' or (not get_content_anws.exists()):
        msg = msg % UCU_TEMPLATE_CONTENT
    else:
        msg = msg % get_content_anws[0].anwser

    send_email(
        from_email=get_email_anws[0].anwser,
        to='adamkuleszaadamkulesza@gmail.com',
        subject='Strike action',
        content=msg
    )

    send_msg_list(MESSAGES['confirm_send_email_ok'],recipient_id)
    clear_session(recipient_id)


def confirm_send_email_discard_response(recipient_id):
    clear_state(recipient_id)
    send_msg_list(MESSAGES['confirm_send_email_discard'],recipient_id)



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

def send_msg_list(text_list,recipient_id):
    for text in text_list:
        send_msg(text,recipient_id).content



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

def show_url_buttons(recipient_id):
    payload = {
        "recipient":{
            "id":recipient_id
        },
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"Click one of the buttons below to get involved!",
                    "buttons":[
                        {
                            "type":"web_url",
                            "url":"https://www.ucu.org.uk/",
                            "title":"Visit the UCU website",
                            "webview_height_ratio": "full"
                        },
                        {
                            "type":"web_url",
                            "url":"https://www.facebook.com/sharer/sharer.php?u=https://www.facebook.com/Nottingham-Student-Solidarity-1615346261890381/",
                            "title":"Share our page",
                            "webview_height_ratio": "compact"
                        }
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

    return requests.post(
        url=fb_api_url,
        headers = {'content-type': 'application/json'},
        data=json.dumps(payload)
    )


def set_state(u_id,state):
    clear_state(u_id)
    State(u_id=u_id,state=state).save()


def clear_state(u_id):
    State.objects.filter(u_id=u_id).delete()


def clear_session(u_id):
    State.objects.filter(u_id=u_id).delete()
    QA.objects.filter(u_id=u_id).delete()


def set_QA(u_id,question,anwser):
    curr_qa = QA.objects.filter(
        u_id=u_id,
        question=question,
    ).delete()

    QA(
        u_id=u_id,
        question=question,
        anwser=anwser,
    ).save()
