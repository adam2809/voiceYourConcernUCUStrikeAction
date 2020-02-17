from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from voiceYourConcern.settings import VERIFY_TOKEN

import json

from rest_framework.exceptions import *

from vyc.utils.vyc_bot_utils import handle_message


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
        
        handle_message(req_body)

        return HttpResponse(status=200)
