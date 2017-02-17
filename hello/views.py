import os
import re
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
HELP_IMAGE_JHS = 'https://s19.postimg.org/9xq4fnjer/jhs.jpg'
HELP_IMAGE_SHS_1 = 'https://s19.postimg.org/3laz5tgcj/shs1.jpg'
HELP_IMAGE_SHS_2 = 'https://s19.postimg.org/t5d9c91qb/shs2.jpg'
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
        for event in events_container.events:
            if event.message.type == 'text':
                try:
                    # remove pain by allow user to not write *
                    clean_text = re.sub('(\d+)([x-z])', r'\g<1>' + '*' + r'\g<2>', event.message.text.lower())
                    clean_text = re.sub('([\)\dx-z])(\()', r'\g<1>' + '*' + r'\g<2>', clean_text)
                    clean_text = re.sub('([\d\)x-z])sqrt', r'\g<1>'+'*sqrt', clean_text)
                    print(clean_text)
                    result = exec_command(clean_text)
                except Exception as e:
                    print(e)
                    print(event.message.text.lower())
                    result = 'Input was error'
            else:
                result = 'We only receive text message'
            if event.message.text.strip() == 'help':
                reply_message = ReplyMessage(event.reply_token, [Message.from_string(result), 
                ImageMessage(HELP_IMAGE_LINK, HELP_IMAGE_REVIEW_LINK),
                ImageMessage(HELP_IMAGE_JHS),
                ImageMessage(HELP_IMAGE_SHS_1),
                ImageMessage(HELP_IMAGE_SHS_2)])
            else:
                reply_message = ReplyMessage(event.reply_token, [Message.from_string(result)])
            res = requests.post(LINE_API_REPLY, data=reply_message.to_json(), headers=LINE_API_HEADERS)
        return HttpResponse(reply_message.to_json())


def _send_push(target_id, message):
    body = dict()
    body['to'] = target_id
    body['messages'] = [Message(message)]
    res = requests.post(LINE_API_PUSH, data=json.dumps(body), headers=LINE_API_HEADERS)
