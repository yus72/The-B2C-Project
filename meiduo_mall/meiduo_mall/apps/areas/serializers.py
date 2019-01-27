# -*- coding: utf-8 -*-
# @Time    : 19-1-26 下午8:47
# @Author  : Yu Shang
# @FileName: serializers.py
# @Software: PyCharm
from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划信息序列化器
    """
    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(serializers.ModelSerializer):
    """
    子行政区划信息序列化器
    """
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')