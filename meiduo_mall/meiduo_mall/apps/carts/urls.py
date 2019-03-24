# -*- coding: utf-8 -*-
# @Time    : 19-1-9 下午6:38
# @Author  : Yu Shang
# @FileName: urls.py
# @Software: PyCharm


from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^cart/$', views.CartView.as_view()),
]
