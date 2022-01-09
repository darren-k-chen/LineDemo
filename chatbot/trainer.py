# Author: Darren K.J. Chen
# E-mail: kjchen@protonmail.ch

import sys; import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from botService import settings

def listToString(ls):
    comma = ', '
    return ('[' + comma.join(ls) + ']')

class BotTrainer:
    def __init__(self):
        pass # ; self.conf = conf
        # self.conf['QnA'] = [self.conf['clientQuestion'], self.conf['clientAnswer']]

    def INIT(self, conf, botNO):
        json_file = open(settings.CONVERSATION_PATH[botNO], 'r', encoding='utf-8')
        json_data = json.load(json_file); json_file.close()
        conf['QnA'] = [conf['clientQuestion'], conf['clientAnswer']]
        json_data[conf['conversationName']].append(conf['QnA'])
        # json_file = open('/home/ubuntu/reas_bot/BotService/botService/chatbot/corpus/conversation.json', 'w', encoding='utf-8')
        # json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        conf['allConversation'] = json_data[conf['conversationName']]
        json_file.close(); chatbot = ChatBot (
            conf['botName'],
            logic_adapters = [
                "chatterbot.logic.BestMatch"
            ]
        ); self.trainer = ListTrainer(chatbot)
        return conf, botNO

    def ALL_TRAIN(self, conf):
        conf, botNO = conf
        for i in conf['allConversation']:
            self.trainer.train(i); print('\n[Debug Msg.] ' + listToString(i) + ' >> Trained' )
        self.trainer.export_for_training(settings.CONVERSATION_PATH[botNO])
        return conf

    def TRAIN(self, conf, startAt=0, endAt=sys.maxsize):
        conf, botNO = conf; counter = -1
        for i in conf['allConversation']:
            counter += 1; print('\n[Debug Msg.] ' + listToString(i) + ' >> Readed\n' )
            if counter >= startAt and counter <= endAt:
                self.trainer.train(i); print('\n[Debug Msg.] ' + listToString(i) + ' >> Trained' )
        self.trainer.export_for_training(settings.CONVERSATION_PATH[botNO])
        return conf

    def TRAIN_NEW_CONVERSATION(self, conf):
        conf, botNO = conf; self.trainer.train(conf['QnA'])
        self.trainer.export_for_training(settings.CONVERSATION_PATH[botNO])
        return conf

    def RESET_TRAINER(self, conf):
        conf = conf[0]
        chatbot = ChatBot (
            conf['botName'],
            logic_adapters = [
                "chatterbot.logic.BestMatch"
            ]
        ); chatbot.storage.drop()
        return conf
