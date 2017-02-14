import os
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from linebot import LineBotApi
# from linebot import WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .models import *
from .worker import exec_command


CHANNEL_ACCESS_TOKEN = os.environ['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = os.environ['CHANNEL_SECRET']
HELP_IMAGE_LINK = 'https://s19.postimg.org/50b2xcdmr/help.jpg'
HELP_IMAGE_REVIEW_LINK = 'https://s19.postimg.org/6gmlfhgjn/help_preview.jpg'
LINE_API_REPLY = "https://api.line.me/v2/bot/message/reply"
LINE_API_PUSH = "https://api.line.me/v2/bot/message/push"
LINE_API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {}".format(CHANNEL_ACCESS_TOKEN)
}
# line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# line_handler = WebhookHandler(CHANNEL_SECRET)


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
            result = exec_command(event.message.text.lower())
        else:
            result = 'We only receive text message'
        if event.message.text.strip() == 'help':
            reply_message = ReplyMessage(event.reply_token, [Message.from_string(result), 
            ImageMessage(HELP_IMAGE_LINK, HELP_IMAGE_REVIEW_LINK)])
        else:
            reply_message = ReplyMessage(event.reply_token, [Message.from_string(result)])
        res = requests.post(LINE_API_REPLY, data=reply_message.to_json(), headers=LINE_API_HEADERS)
        print res.text
        return HttpResponse(reply_message.to_json())


def _send_push(target_id, message):
    body = dict()
    body['to'] = target_id
    body['messages'] = [Message(message)]
    res = requests.post(LINE_API_PUSH, data=json.dumps(body), headers=LINE_API_HEADERS)
