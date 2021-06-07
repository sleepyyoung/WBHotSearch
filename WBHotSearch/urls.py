"""WBHotSearch URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path, include, reverse
from WBHotSearch import settings

urlpatterns = [
    path('the_admin/', admin.site.urls),
    path('', include(("home.urls", "home"), namespace="home")),
    path('api/', include(("api.urls", "api"), namespace="api")),
    path('', include(("enter.urls", "enter"), namespace="enter")),
    path('captcha/', include("captcha.urls")),
]

# -------------------------------------------------------------------------
# /home/sleepyyoung/shScripts/scrapy_weiboSpider.sh
# #! /bin/sh
# export PATH=$PATH:/usr/local/bin
#
# echo $PATH
# cd /home/sleepyyoung/Django-Object/WBHotSearch/DataSpider
# /home/sleepyyoung/anaconda3/bin/scrapy crawl weiboSpider >> weiboSpider.log 2>&1 &
#
# crontab -e
"""
#! /bin/sh
export PATH=$PATH:/usr/local/bin

echo $PATH
cd /home/sleepyyoung/Django-Object/WBHotSearch/DataSpider
/home/sleepyyoung/anaconda3/bin/scrapy crawl weiboSpider >> weiboSpider.log 2>&1 &
"""
# * * * * * sh /home/sleepyyoung/Django-Object/WBHotSearch__S/DataSpider/scrapy_weiboSpider.sh
# 每隔一分钟运行一次
# 日志位置： /var/log/cron.log
# service cron start
# service cron status
# service cron stop
# -------------------------------------------------------------------------

# 定时运行爬虫

# from apscheduler.schedulers.background import BackgroundScheduler
# import os
#
#
# def tick():
#     spider_path = os.getcwd()
#     if spider_path.split("/")[-1] == "wblsrs" or spider_path.split("\\")[-1] == "wblsrs":
#         os.system("cd DataSpider && scrapy crawl weiboSpider")
#     else:
#         print("ERROR")
#
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(tick, 'interval', seconds=60)
# scheduler.start()

# Linux 上定时运行爬虫
# crontab -e  # 编辑任务 
# * * * * * sh /home/sleepyyoung/wblsrs/DataSpider/scrapy_weiboSpider.sh
# crontab -l  # 查看任务
# crontab -r  # 删除任务



