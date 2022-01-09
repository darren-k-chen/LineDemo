# Author: Darren K.J. Chen
# E-mail: kjchen@protonmail.ch

import time as t
import schedule, random, threading, json, requests

from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from chatbot.respondent import Respondent
from chatbot.trainer import BotTrainer

import linebot.account

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

class LinebotService:
    def __init__(self, botNO):
        self.botNO = botNO
        ( self.line_bot_api, self.parser ) = (
            LineBotApi (
                settings.LINE_CHANNEL['ACCESS_TOKEN'][self.botNO],
                timeout = 180
            ), WebhookParser (
                settings.LINE_CHANNEL['SECRET'][self.botNO]
            ),
        ); th = threading.Thread(target = self.scheduleService); th.start()
        # self.scheduleService()

    @csrf_exempt
    def botService(self, request):
        if request.method == 'POST':
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            body = request.body.decode('utf-8')

            try:
                events = self.parser.parse(body, signature)
            except InvalidSignatureError:
                return HttpResponseForbidden()
            except LineBotApiError:
                return HttpResponseBadRequest()

            for event in events:
                msgReply = 'defalutMsg'
                if isinstance(event, MessageEvent):
                    if '@冠儒' in event.message.text:
                        self.line_bot_api.reply_message (
                            event.reply_token,
                            TextSendMessage(text=msgReply)
                        )
                    elif event.source.type == "user":
                        # if '註冊' in event.message.text:
                        #
                        profile = self.line_bot_api.get_profile (
                            event.source.user_id
                        ); print(profile.display_name); print(type(profile.display_name))
                        try:
                            msgPUSH = profile.display_name + ' 留言給冠儒：\n' + event.message.text + '\n\nUserID: ' + profile.user_id
                        except:
                            msgPUSH = 'exceptEvent: ' + profile.display_name + ' 以非文字格式傳了訊息給您！\n\nUserID: ' + profile.user_id
                        self.line_bot_api.push_message (
                            'Cf7bb5c05288433dae62584999121acd0',
                            TextSendMessage ( text = msgPUSH )
                        ); print('[DEBUG] >> ' + msgPUSH)
                        # print(profile); print(type(profile))
                        # json_file = open(settings.STATIC_ROOT+'/msg_history.json', 'r', encoding='utf-8')
                        # json_data = json.load(json_file); json_file.close()
                        # profile = json.load(profile)
                        # json_data["msg_history"].append (
                        #     {
                        #         "usr_msg": event.message.text,
                                # "usr_profile": str(profile)
                                # "usr_name" : profile["displayName"],
                                # "usr_id"   : profile["userId"],
                                # "usr_msg"  : event.message.text
                            # }
                        # ); # json_data["msg_history"].append(profile)
                        # json_file = open(settings.STATIC_ROOT+'msg_history.json', 'w', encoding='utf-8')
                        # json.dump(json_data, json_file, indent=4, ensure_ascii=False)
                        # json_file.close(); print(json_data)
                    # elif event.source.type == "group":
                    #     summary = self.line_bot_api.get_group_summary (
                    #         event.source.group_id
                    #     ); print(type(summary)); print(summary); print((summary.text)); print(summary.text)

            return HttpResponse()
        else: return HttpResponseBadRequest()

    def broadcastMsg(self, msgType='txt', msgContent='defalutContent'):
        if msgType == 'img':
            msgContent = ImageSendMessage (
                original_content_url=msgContent,
                preview_image_url=msgContent
            )
        elif msgType == 'txt':
            msgContent = TextSendMessage(text=msgContent)
        else: msgContent = TextSendMessage(text='ErrorMsgType')
        # self.line_bot_api.broadcast(msgContent)
        for i in settings.FAMILY_GROUP:
            self.line_bot_api.push_message(i, msgContent)

    def morningGreeting(self):
        greetingImg = 'https://www.crazybless.com/good-morning/morning/image/%E6%97%A9%E5%AE%89%E5%9C%96%E4%B8%8B%E8%BC%89%20(' + str(random.randint(1, 1000)) + ').jpg'
        self.broadcastMsg (
            msgType = 'img',
            msgContent = greetingImg
        ); weatherData = self.getWeatherData(); # self.setNewTime();
        todayWeather = weatherData[0]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
        weatherMsg  = '今天' + weatherData[0]["locationName"] + '的天氣' + todayWeather
        if '雨' in todayWeather:
            weatherMsg += '，出門記得帶把傘！'
        elif '晴' in todayWeather:
            weatherMsg += '，天氣不錯，記得多出去走一走！'
        self.broadcastMsg (
            msgContent = weatherMsg
        ); # return schedule.CancelJob

    def timedMsg(self, frequency='day', time='08:08'):
        if frequency == 'day': schedule.every().day.at(time).do(self.morningGreeting)
        else: pass

    def botStatus(self, request):
        html = "<center><h1>Service is Work!!</h1></center><p>"
        return HttpResponse(html)

    def resetNewTime(self, request):
        # newTime = '22:22'
        # newTime = str(random.randint(22, 23)) + ':' + str(random.randint(10, 59))
        self.timedMsg (
            # job  = self.morningGreeting(),
            # time = newTime
            time = settings.NEW_TIME
        ); html = '<center><h1> Modified to New Time: ' + settings.NEW_TIME + '</h1></center><p>'
        return HttpResponse(html)

    # def setNewTime(self):
    #     newTime = '22:22'; self.timedMsg (
    #         time = newTime
    #     )

    def scheduleService(self):
        while True:
            schedule.run_pending()
            t.sleep(1)

    def getWeatherData(self):
        # url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + settings.OPEN_WEATHER_DATA_TOKEN + '&format=JSON&locationName=' + city
        url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName=桃園市&elementName=Wx&Authorization=' + settings.OPEN_WEATHER_DATA_TOKEN
        # url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName=桃園市&elementName=Wx&Authorization=CWB-D7E87A9F-817D-4DB6-AFCD-84F8A67A3F38'
        payload={}; files={}; headers = {
            'Cookie': 'TS01dbf791=0107dddfef10e2453bd6b48d9f5de5c9d8a3cb27d7cfd35165ae10cde26b48d2f4620468247a5911433be66b69ef756021953bace6'
        }; weatherData = requests.request("GET", url, headers=headers, data=payload, files=files)
        # weatherData = requests.get(url)
        weatherData = (json.loads(weatherData.text,encoding='utf-8'))["records"]["location"]
        return weatherData



    # def listToString(self, ls):
    #     comma = ', '
    #     return ('[' + comma.join(ls) + ']')
