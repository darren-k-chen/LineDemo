from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from ..BotService.chatbot.respondent import Respondent
from ..BotService.chatbot.trainer import BotTrainer

# import sys; sys.path.append('/home/ubuntu/.pyenv/versions/3.6.5/lib/python3.6/site-packages')
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def botService(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                mtext=event.message.text
                message=[]
                message.append(TextSendMessage(text=mtext))
                line_bot_api.reply_message(event.reply_token,message)
        return HttpResponse()
    else: return HttpResponseBadRequest()

def botStatus(request):
    timeNow = datetime.datetime.now()
    html = "<center><h1>Service is Work!!</h1><p><h5>It is now %s.</h5></center>" % timeNow
    return HttpResponse(html)

# Create your views here.
# class BotService(View):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse({
#             'TEST': 'testMsg_byDarren'
#         })
