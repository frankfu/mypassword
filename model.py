# -*- coding: utf-8 -*-
import web
import datetime
import hashlib
from os.path import join

db = web.database(dbn='sqlite', db=join("data", "mypassword.db3"))

def list_post(tag = ''):
    if not tag:
        return db.select('posts', what = 'id, name, address, username, password, tag, datetime(updated) as updated, datetime(created) as created', order = 'id DESC')
    else:
        return db.select('posts', what = 'id, name, address, username, password, tag, datetime(updated) as updated, datetime(created) as created', where = 'tag = $tag', order = 'id DESC', vars = locals())

def list_tag():
    return db.select('posts', what = 'distinct tag')

def view_post(post_id):
    post = db.select('posts', what = 'id, name, address, username, password, tag, datetime(updated) as updated, datetime(created) as created', where = "id = $post_id", vars = locals())[0]
    return post

def new_post(name, address, username, password, tag):
    return db.insert('posts', name = name, address = address, username = username, password = password, tag = tag, updated = datetime.datetime.utcnow(), created = datetime.datetime.utcnow())

def edit_post(form):
    return db.update('posts', 'id = $form.d.id', name = form.d.name, address = form.d.address, username = form.d.username, password = form.d.password, tag = form.d.tag, updated = datetime.datetime.utcnow(), vars=locals())

def delete_post(post_id):
    return db.delete('posts', 'id = $post_id', vars=locals())

def accept_list():
    return [i.code for i in db.select('codes', what = 'code', where = 'accept = 1')]

def new_code(code):
    return db.insert('codes', code = code, accept = 0)

def accept_code(code):
    return db.update('codes', "code = $code", accept = 1, vars=locals())

def delete_code(code_id):
    return db.delete('codes', 'id = $code_id', vars=locals())
