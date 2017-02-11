import re

import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .worker import parse

CHANNEL_ACCESS_TOKEN = "xjNlgBf2p8rHke5W5iu/gNXjci1p0navxxgqyK3CRPVdHRvFoWhd9QT7YK/YqAlhU7eXAK3Sb91X3DAGv67jn9vGIgjHMBnGtZ7U019Xa2gQeHMvd1vg6LCscRw5EqS+5KcC7+RZV9QcRX8nfLkBLwdB04t89/1O/w1cDnyilFU="
LINE_API_REPLY = "https://api.line.me/v2/bot/message/reply"


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})


@csrf_exempt
def linebot(request):
    if request.method == 'POST':
        events_container = EventsContainer(request.body)
        event = events_container.events[0]
        if event.message.type == 'text':
            result = _exec_command(event.message.text.lower())
        else:
            result = 'We only receive text message'
        reply_message = ReplyMessage(event.reply_token, [Message.from_string(result)])
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(CHANNEL_ACCESS_TOKEN)
        }
        res = requests.post(LINE_API_REPLY, data=reply_message.to_json(), headers=headers)
        print res.text
        return HttpResponse(reply_message.to_json())


def _exec_command(message):
    if 'help' in message:
        return 'Help page is under construction'
    else:
        return parse(message)
