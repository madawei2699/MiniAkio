#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import static_file, redirect, response, request

from utils import template, get_auth_user, is_password
from blog import blog
from admin import admin
from picky import picky
from models import Author
from config import SECRET


@blog.route('/static/<fileext>/<filename:path>')
def send_static(fileext, filename):
    return static_file(filename, root='static/%s' % fileext)


@blog.route("/auth/login", method='GET')
def get_admin_login():
    if get_auth_user():
        redirect('/admin')
    return template("admin/login.html")


@blog.route("/auth/login", method='POST')
def post_admin_login():
    email = request.forms.get('email').decode('utf-8')
    password = request.forms.get('password').decode('utf-8')
    try:
        user = Author.get(email=email)
    except Author.DoesNotExist:
        redirect('/auth/login')
    enpass = user.password
    if is_password(password, enpass):
        response.set_cookie("user", user.id, secret=SECRET, path="/",
                            max_age=30 * 24 * 60 * 60)
        redirect('/admin')
    else:
        redirect('/auth/login')


@blog.route("/auth/logout", method='GET')
def admin_logout():
    response.delete_cookie("user", path='/')
    redirect('/')


blog.mount(admin, "/admin")
blog.mount(picky, "/picky")
