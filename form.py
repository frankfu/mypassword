# -*- coding: utf-8 -*-
import web
import hashlib

username = "admin"
password = "ff63da1131295204bc85953c0d21a049202e33ca"

def login_form():
    return web.form.Form(
        web.form.Textbox("username", web.form.notnull, size=20, description="用户名："),
        web.form.Password("password", web.form.notnull, size=20, description="密码："),
        web.form.Button(u"登录"),
        validators = [web.form.Validator("用户名或密码不匹配",
                                         lambda i: i.username in username and hashlib.sha1(i.password).hexdigest() in password)]
        )

def email_sent_form():
    return web.form.Form(
        web.form.Textbox("address", web.form.notnull, size=30, description="邮箱："),
        web.form.Button(u"确定")
        )

def post_add_form(post_id='', post_name='', post_address='', post_username='', post_password='', post_tag=''):
    return web.form.Form(
        web.form.Textbox("name", web.form.notnull, size=30, description="名称：", value=post_name),
        web.form.Textbox("address", web.form.notnull, size=30, description="地址：", value=post_address),
        web.form.Textbox("username", web.form.notnull, size=30, description="用户名：", value=post_username),
        web.form.Textbox("password", web.form.notnull, size=30, description="密码：", value=post_password),
        web.form.Textbox("tag", web.form.notnull, size=30, description="标签：", value=post_tag),
        web.form.Hidden('id', value=post_id),
        web.form.Button(u"确定")
        )
