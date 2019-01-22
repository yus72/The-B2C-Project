# -*- coding: utf-8 -*-
# @Time    : 19-1-21 下午5:52
# @Author  : Yu Shang
# @FileName: urls.py
# @Software: PyCharm

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
    url(r'^qq/user/$', views.QQAuthUserView.as_view()),

]