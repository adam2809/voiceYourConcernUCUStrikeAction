from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from voiceYourConcern.settings import VERIFY_TOKEN

import json

from vyc.vyc_bot_utils import respond_to_msg,respond_to_get_started


class FacebookWebhooks(CreateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookWebhooks, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        hub_challenge = request.GET['hub.challenge']
        hub_mode = request.GET['hub.mode']
        verify_token_matches = request.GET['hub.verify_token'] == VERIFY_TOKEN

        if hub_mode and verify_token_matches:
            return HttpResponse(hub_challenge,200)

        return HttpResponse(status=403)


    def post(self, request, *args, **kwargs):
        req_body = json.loads(request.read().decode('utf-8'))

        # TODO return an error if something goes wrong in respond_to_msg or any of the ifs fail
        if req_body['object'] == 'page':
            for entry in req_body['entry']:
                for event in entry['messaging']:
                    if 'postback' in event and event['postback']['title'] == 'Get Started':
                        respond_to_get_started(event)
                        continue

                    if event['message'] and event['message']['text']:
                        respond_to_msg(event)
                        continue

        return HttpResponse(status=200)
