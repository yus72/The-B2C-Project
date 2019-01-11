# -*- coding: utf-8 -*-
# @Time    : 18-12-3 下午5:05
# @Author  : Yu Shang
# @FileName: constants.py
# @Software: PyCharm

# 图片验证码的redis有效期，单位：秒
IMAGE_CODE_REDIS_EXPIRES = 5 * 60


#短信验证码有效期
SMS_CODE_REDIS_EXPIRES = 5 * 60


# 短信验证码发送间隔
SEND_SMS_CODE_INTERVAL = 60

# 模板的ID
SMS_CODE_TEMP_ID = 1