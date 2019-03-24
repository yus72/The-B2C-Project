# -*- coding: utf-8 -*-
# @Time    : 19-3-18 上午10:53
# @Author  : Yu Shang
# @FileName: pagination.py
# @Software: PyCharm

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    # 默认条数
    page_size = 2

    # 指明前端的参数名
    page_size_query_param = 'page_size'

    max_page_size = 20