from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class FacebookWebhooks(CreateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(FacebookWebhooks, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
            print("what the fuck")
            return HttpResponse('hi im a get endpoint')

    def post(self, request, *args, **kwargs):
        return HttpResponse('hi im a post endpoint')
