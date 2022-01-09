# Author: Darren K.J. Chen
# E-mail: kjchen@protonmail.ch

import os; import sys; import json

from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer #, ChatterBotCorpusTrainer
from trainer import BotTrainer

class ReasBOT:
    conf = { # <conf> aka. config INFO
        'botName': sys.argv[1],
        'conversationName': 'testConversation',
        'clientQuestion': sys.argv[2],
        'clientAnswer': sys.argv[3],
        'QnA': list(),
        'trainedMsg': list(),
        'allConversation': dict(),
        'logic_adapters': [
            "chatterbot.logic.BestMatch"
        ]
    }

    chatbot = ChatBot (
        conf['botName'],
        logic_adapters = conf['logic_adapters']
    )

    def __init__(self):
        print('\n======= Pre-Train =======\n')
        print(self.chatbot.get_response(self.conf['clientQuestion']))
        print('\n=========================\n')

        trainer = BotTrainer(self.conf)
        self.conf = trainer.TRAIN()

    def replyMsg(self):
        print('\n======== Trained ========\n')
        print(self.chatbot.get_response(self.conf['clientQuestion']))
        print('\n=========================\n')

if __name__ == '__main__':
    bot = ReasBOT(); print(bot.replyMsg())
