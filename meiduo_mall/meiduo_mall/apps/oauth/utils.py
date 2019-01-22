# -*- coding: utf-8 -*-
# @Time    : 19-1-21 下午5:11
# @Author  : Yu Shang
# @FileName: utils.py
# @Software: PyCharm

from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
import json
from django.conf import settings
import logging

from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData
from oauth import constants
from .exceptions import OAuthQQAPIError

logger = logging.getLogger('django')


class OAuthQQ(object):
    """
    QQ认证辅助工具类
    """
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id if client_id else settings.QQ_CLIENT_ID
        self.redirect_uri = redirect_uri if redirect_uri else settings.QQ_REDIRECT_URI
        self.state = state if state else settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径
        # self.state = state or settings.QQ_STATE
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET


    def get_login_url(self):
        """
        获取qq登录的网址
        :return: url网址
        """

        url = 'https://graph.qq.com/oauth2.0/authorize?'

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
        }

        url += urlencode(params)
        return url

    def get_access_token(self, code):
        """
        获取access_token
        :param code: qq提供的code
        :return: access_token
        """

        url = 'https://graph.qq.com/oauth2.0/token?'


        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        url += urlencode(params)

        try:
            # 发送请求
            resp = urlopen(url)

            # 获取数据
            resp_data = resp.read().decode()

            #解析access_token
            resp_dict = parse_qs(resp_data)
        except Exception as e:
            logger.error('获取access_token异常：%s' % e)
            raise OAuthQQAPIError
        else:
            access_token = resp_dict.get('access_token')

            return access_token[0]


    def get_openid(self, access_token):
        """
        获取用户的openid
        :param access_token: qq提供的access_token
        :return: open_id
        """
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token

        try:
            # 发送请求
            resp = urlopen(url)

            # 获取数据
            resp_data = resp.read().decode()

            # 解析access_token
            # 返回的数据 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            resp_data = resp_data[10:-4]
            resp_dict = json.loads(resp_data)

        except Exception as e:
            logger.error('获取openid异常：%s' % e)
            raise OAuthQQAPIError
        else:
            openid = resp_dict.get('openid')

            return openid

    def generate_bind_user_access_token(self, openid):
        """
        生成保存用户数据的token
        :param openid: 用户的openid
        :return: token
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.BIND_USER_ACCESS_TOKEN_EXPIRES)
        data = {'openid': openid}
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_bind_user_access_token(access_token):
        """
        检验保存用户数据的token
        :param access_token: token
        :return: openid or None
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.BIND_USER_ACCESS_TOKEN_EXPIRES)
        try:
            data = serializer.loads(access_token)
        except BadData:
            return None
        else:
            return data['openid']

