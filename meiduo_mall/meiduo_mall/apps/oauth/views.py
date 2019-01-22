from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.exceptions import OAuthQQAPIError
from oauth.models import OAuthQQUser
from oauth.serializers import OAuthQQUserSerializer
from .utils import OAuthQQ


#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
class QQAuthURLView(APIView):
    """
    获取QQ登录的url
    """
    def get(self, request):
        """
        提供用于qq登录的url
        """

        # 获取next参数
        next = request.query_params.get('next')

        # 拼接QQ网址
        oauth_qq = OAuthQQ(state=next)
        login_url = oauth_qq.get_login_url()

        # 返回
        return Response({'login_url': login_url})


# url(r'^qq/user/$', views.QQAuthUserView.as_view()),
class QQAuthUserView(CreateAPIView):
    """
    QQ登录的用户
    """

    serializer_class = OAuthQQUserSerializer

    def get(self, request):
        """
        获取qq登录的用户数据
        """

        # 获取code
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取用户access_token
        oauth_qq = OAuthQQ()

        try:
            access_token = oauth_qq.get_access_token(code)
        except OAuthQQAPIError:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 获取用户的openid
        try:
            openid = oauth_qq.get_openid(access_token)
        except OAuthQQAPIError:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据openid查询数据库，判断用户是否存在
        try:
            oauth_qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 用户第一次使用QQ登录
            access_token = oauth_qq.generate_bind_user_access_token(openid)
            return Response({'access_token': access_token})
        else:
            # 找到用户, 生成token
            user = oauth_qq_user.user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })
            return response



