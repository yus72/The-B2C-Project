# -*- coding: utf-8 -*-
# @Time    : 18-12-4 下午6:55
# @Author  : Yu Shang
# @FileName: tasks.py
# @Software: PyCharm
import logging

from celery_tasks.main import celery_app
from .utils.yuntongxun.sms import CCP

logger = logging.getLogger("django")


@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, expires, temp_id):
    """
    发送短信验证码
    :param mobile: 手机号
    :param sms_code: 验证码
    :param expires: 有效期
    :return: None
    """
    # try:
    #     ccp = CCP()
    #     result = ccp.send_template_sms(mobile, [sms_code, expires], temp_id)
    # except Exception as e:
    #     logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    # else:
    #     if result == 0:
    #         logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
    #     else:
    #         logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
    print(sms_code)