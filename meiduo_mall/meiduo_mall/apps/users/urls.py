# -*- coding: utf-8 -*-
# @Time    : 19-1-9 下午6:38
# @Author  : Yu Shang
# @FileName: urls.py
# @Software: PyCharm


from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
]