# -*- coding: utf-8 -*-
# @Time    : 18-12-4 下午4:26
# @Author  : Yu Shang
# @FileName: serializers.py
# @Software: PyCharm
from django_redis import get_redis_connection
from redis import RedisError
from rest_framework import serializers
import logging

logger =  logging.getLogger('django')


class ImageCodeCheckSerializer(serializers.Serializer):
    '''
    图片验证码校验序列化器
    '''

    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        """
        校验
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']


        # 查询真实图片验证码
        redis_conn = get_redis_connection('verify_codes')
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)
        if not real_image_code_text:
            raise serializers.ValidationError('图片验证码无效')

        # 删除redis中图片验证码
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            logger.error(e)


        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode()
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')


        # 判断是否在60s内
        # get_serializer 方法在创建序列化器对象的时候，会补充context属性
        # context属性中会包含三个值  request, format, view 类视图对象

        # django中的类视图对象中，kwargs保存了路径中提取出来的参数


        mobile = self.context['view'].kwargs['mobile']

        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs