import random

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
import logging
from rest_framework import status


from . import constants
from .serializers import ImageCodeCheckSerializer
from meiduo_mall.utils.yuntongxun.sms import CCP


logger = logging.getLogger('django')

# Create your views here.
class ImageCodeView(APIView):
    '''图片验证码'''

    def get(self,request, image_code_id):

        # 生成图片验证码
        text, image = captcha.generate_captcha()

        # 保存真实值
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex("img_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)


        # 返回图片给前端

        return HttpResponse(image, content_type='image/jpg')


# url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
class SMSCodeView(GenericAPIView):
    """
    短信验证码
    传入参数：
        mobile, image_code_id, text
    """
    serializer_class = ImageCodeCheckSerializer

    def get(self, request, mobile):
        #校验参数  由序列化器完成
        serializer = self.get_serializer(data = request.query_params)
        serializer.is_valid(raise_exception = True)


        #生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        print(sms_code)


        #保存短信验证码  保存短信发送记录，以便在序列化器中校验
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # redis_conn.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        #redis管道
        pl = redis_conn.pipeline()
        pl.setex("sms_%s" % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex("send_flag_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        #发送短信
        # try:
        #     expires = str(constants.SMS_CODE_REDIS_EXPIRES // 60)
        #     ccp = CCP()
        #     result = ccp.send_template_sms(mobile, [sms_code, expires], constants.SMS_CODE_TEMP_ID)
        # except Exception as e:
        #     logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
        #     return Response({"message": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # else:
        #     if result == 0:
        #         logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        #         return Response({"message": "OK"})
        #     else:
        #         logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
        #         return Response({"message": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "OK"})

