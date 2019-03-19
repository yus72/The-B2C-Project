# -*- coding: utf-8 -*-
# @Time    : 19-3-18 上午10:35
# @Author  : Yu Shang
# @FileName: serializers.py
# @Software: PyCharm
from rest_framework import serializers
from goods.models import SKU


class SKUSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')
