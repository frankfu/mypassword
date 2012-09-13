# -*- coding: utf-8 -*-
import web
import model
import form
import util
import settings

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

urls = (
  '/', 'index',
  '/tag/(.*)', 'tag',
  '/login', 'login',
  '/logout', 'logout',
  '/add', 'add',
  '/view/(\d+)', 'view',
  '/edit/(\d+)', 'edit',
  '/delete/(\d+)', 'delete',
  '/accept/(.*)', 'accept',
  '/share', 'share')

app = web.application(urls, globals(), autoreload=True)

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'user': 'anonymous'})
    web.config._session = session
else:
    session = web.config._session

def render(params = {}, partial = False):
    global_vars = dict(settings.GLOBAL_PARAMS.items() + params.items())

    if partial:
        return web.template.render('templates/', globals=global_vars)
    else:
        return web.template.render('templates/', base='layout', globals=global_vars)

class about:
    def GET(self):
        return render({'title': settings.SITE_NAME}).about()

class index:
    def GET(self):
        cookies = web.cookies(accept_str = '')
        if session.user == 'admin' or (cookies.accept_str != '' and cookies.accept_str in model.accept_list()):
            posts = model.list_post()
            tags = model.list_tag()
            return render({'title': settings.SITE_NAME}).list(session.user, tags, posts)
        else:
	    return render({'title': settings.SITE_NAME}).notauth()

class tag:
    def GET(self, tag):
        cookies = web.cookies(accept_str = '')
        if session.user == 'admin' or (cookies.accept_str != '' and cookies.accept_str in model.accept_list()):
            posts = model.list_post(tag)
            tags = model.list_tag()
            return render({'title': settings.SITE_NAME}).list(session.user, tags, posts)
        else:
	    return render({'title': settings.SITE_NAME}).notauth()

class add:
    def GET(self):
        if session.user == 'admin':
            f = form.post_add_form()
            return render({'title': settings.SITE_NAME}).add(f)
        else:
	    return render({'title': settings.SITE_NAME}).notauth()

    def POST(self):
        if session.user == 'admin':
            f = form.post_add_form()
            if not f.validates():
                return render({'title': settings.SITE_NAME}).add(f)
            else:
                post_id = model.new_post(f.d.name, f.d.address, f.d.username, f.d.password, f.d.tag)
                if post_id:
                    return web.redirect("/view/%d" % post_id)
                else:
                    return render({'title': settings.SITE_NAME}).failed()
        else:
	    return render({'title': settings.SITE_NAME}).notauth()

class view:
    def GET(self, post_id):
        if session.user == 'admin':
            post_id = int(post_id)
            post = model.view_post(post_id)
            return render({'title': settings.SITE_NAME}).view(post)
        else:
	    return render({'title': settings.SITE_NAME}).notauth()

class edit:
    def GET(self, post_id):
        if session.user == 'admin':
            post_id = int(post_id)
            post = model.view_post(post_id)
            f = form.post_add_form(post.id, post.name, post.address, post.username, post.password, post.tag)
            return render({'title': settings.SITE_NAME}).edit(f)
        else:
	    return render({'title': settings.SITE_NAME}).notauth()
    
    def POST(self, post_id):
        if session.user == 'admin':
            post_id = int(post_id)
            post = model.view_post(post_id)
            f = form.post_add_form(post.id, post.name, post.address, post.username, post.password, post.tag)
            if not f.validates():
                return render({'title': settings.SITE_NAME}).edit(f)
            else:
                r = model.edit_post(f)
                if r:
                    return web.redirect("/edit/%d" % post_id)
                else:
                    return render({'title': settings.SITE_NAME}).failed()
        else:
	    return render({'title': settings.SITE_NAME}).notauth()

class delete:
    def GET(self, post_id):
        if session.user == 'admin':
            post_id = int(post_id)
            r = model.delete_post(post_id)
            if r:
                return web.redirect("/")
        else:
	    return render({'title': settings.SITE_NAME}).notauth()

class share:
    def GET(self):
        if session.user == 'admin':
            f = form.email_sent_form()
            return render({'title': settings.SITE_NAME}).share(f, '')
        else:
	    return render({'title': settings.SITE_NAME}).notauth()
    
    def POST(self):
        f = form.email_sent_form()
        if not f.validates():
            return render({'title': settings.SITE_NAME}).share(f, 'failure')
        else:
            for recip in f.d.address.replace(' ', '').split(';'):
                if recip:
                    accept_str = util.accept_code()
                    model.new_code(accept_str)
                    util.sendmail(f.d.address, accept_str)
            return render({'title': settings.SITE_NAME}).share(f, 'success')

class login:
    def GET(self):
        f = form.login_form()
        return render({'title': settings.SITE_NAME}).login(session.user, f)
    
    def POST(self):
        f = form.login_form()
        if not f.validates():
            return render({'title': settings.SITE_NAME}).login(session.user, f)
        else:
            session.user = f['username'].value
            return web.redirect("/")

class accept:
    def GET(self, accept_str):
        if accept_str in model.accept_list():
            return render({'title': settings.SITE_NAME}).notaccept()
        else:
            model.accept_code(accept_str)
            web.setcookie('accept_str', accept_str, settings.EXPIRES)
            raise web.redirect('/')

class logout:
    def GET(self):
        session.kill()
        raise web.redirect('/login')

if __name__ == "__main__":
    app.run()
