# -*- coding: utf-8 -*-
# @Time    : 19-1-9 下午6:38
# @Author  : Yu Shang
# @FileName: urls.py
# @Software: PyCharm


from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views


urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    url(r'^users/$', views.UserView.as_view()),
    url(r'^authorizations/$', obtain_jwt_token), # 登陆认证
    url(r'^user/$', views.UserDetailView.as_view()), # 个人中心的基本信息
    url(r'^email/$', views.EmailView.as_view()), # 发送email
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    url(r'^browse_histories/$', views.UserBrowsingHistoryView.as_view())
]

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')

urlpatterns += router.urls