from django.core.management.base import BaseCommand
from voiceYourConcern.settings import FB_KEY

import requests
import json

fb_api_url = f'https://graph.facebook.com/v2.6/me/messenger_profile?access_token={FB_KEY}'

class Command(BaseCommand):
    def handle(self,*args,**options):
        payload_persistant_menu = {
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": 'false',
                    "call_to_actions": [
                        {
                            "type": "postback",
                            "title": "Send email to admninistration",
                            "payload": "send_email/yes"
                        }
                    ]
                }
            ]
        }

        payload_get_started = {
            "get_started": {
                "payload": "get_started/none"
            }
        }

        payload_greeting = {
            "greeting": [
                {
                    "locale":"default",
                    "text":"Get involved in strike action as a student!"
                },
            ]
        }

        for payload in [payload_persistant_menu,payload_get_started,payload_greeting]:
            print(requests.post(
                url=fb_api_url,
                headers = {'content-type': 'application/json'},
                data=json.dumps(payload)
            ).content)
