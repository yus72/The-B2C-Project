# -*- coding: utf-8 -*-
# @Time    : 18-12-3 下午5:11
# @Author  : Yu Shang
# @FileName: urls.py
# @Software: PyCharm


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
]


