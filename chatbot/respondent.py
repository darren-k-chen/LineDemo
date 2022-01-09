# Author: Darren K.J. Chen
# E-mail: kjchen@protonmail.ch

import os; import sys; import json
from chatterbot import ChatBot

class Respondent:
    def __init__(self):
        pass

    def replyMsg(self, conf):
        chatbot = ChatBot (
            conf['botName'],
            logic_adapters = conf['logic_adapters']
        )
        print('\n======== Replyed ========\n')
        replyMsg = str(chatbot.get_response(conf['clientQuestion']))
        print(replyMsg); return replyMsg
        # print('\n=========================\n')
