import json

from django.db import models


# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class Message:
    def __init__(self, message):
        self.text = message['text']
        self.type = message['type']
        self.id = message['id']
        self._message = message

    def to_dict(self):
        return self._message


class Source:
    def __init__(self, source):
        self.type = source['type']
        self.user_id = source['userId']
        self._source = source

    def to_dict(self):
        return self._source


class Event:
    def __init__(self, reply_token, message, type, timestamp, source):
        self.reply_token = reply_token
        self.message = Message(message)
        self.type = type
        self.timestamp = timestamp
        self.source = Source(source)


class EventsContainer:
    def __init__(self, _json):
        self.events = []
        data = json.loads(_json)
        for event in data['events']:
            event_item = Event(event['replyToken'], event['message'],
                               event['type'], event['timestamp'], event['source'])
            self.events.append(event_item)


class ReplyMessage:
    def __init__(self, reply_token, messages):
        self.reply_token = reply_token
        self.messages = messages

    def to_dict(self):
        temp = dict()
        temp['replyToken'] = self.reply_token
        messages_temp = []
        for message in self.messages:
            messages_temp.append(message.to_dict())
        temp['messages'] = messages_temp
        return temp

    def to_json(self):
        temp = dict()
        temp['replyToken'] = self.reply_token
        messages_temp = []
        for message in self.messages:
            messages_temp.append(message.to_dict())
        temp['messages'] = messages_temp
        return json.dumps(temp)
