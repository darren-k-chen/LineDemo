""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Author: Darren K.J. Chen
# E-mail: kjchen@protonmail.ch

from django.urls import path
from django.conf import settings
from . import views

bot = list()
if len(settings.LINE_CHANNEL['ACCESS_TOKEN']) == len(settings.LINE_CHANNEL['SECRET']):
    for i in range(len(settings.LINE_CHANNEL['ACCESS_TOKEN'])):
        bot.append(views.LinebotService(i))
else: print('[Debug Msg.] [Line Msg. API] ACCESS_TOKEN Amount not equal SECRET Amount')

urlpatterns = [
    path('', bot[0].botStatus, name='botStatus-00'),
    path('bot-00', bot[0].botService, name='botService-00'),
    path('resetNewTime', bot[0].resetNewTime, name='resetNewTime'),
    # path('bot-01', bot[1].botService, name='botService-01'),
]
