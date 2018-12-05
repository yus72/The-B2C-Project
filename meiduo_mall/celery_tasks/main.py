# -*- coding: utf-8 -*-
# @Time    : 18-12-4 下午6:54
# @Author  : Yu Shang
# @FileName: main.py
# @Software: PyCharm

from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# 创建celery应用
celery_app = Celery('meiduo')

# 导入celery配置
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
