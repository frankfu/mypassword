# -*- coding: utf-8 -*-

SITE_NAME = '用户名、密码 —— 记事本'
SITE_URL = 'http://50.116.3.14:8080'
EXPIRES = 2592000

FROM = 'frankz993@gmail.com'
SUBJECT = '认证邮件'
MESSAGE = '通过此认证连接：%s，您可获得一个月的有效访问期。'

GLOBAL_PARAMS = { 'site_name' : SITE_NAME }
