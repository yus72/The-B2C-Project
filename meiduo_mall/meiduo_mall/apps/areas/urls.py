# -*- coding: utf-8 -*-
# @Time    : 19-1-9 下午6:38
# @Author  : Yu Shang
# @FileName: urls.py
# @Software: PyCharm


from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [

]

router = DefaultRouter()
router.register('areas', views.AreasViewSet, base_name='areas')
urlpatterns += router.urls