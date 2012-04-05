#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, redirect, request
from utils import template, authenticate, hexpassword, is_password
from models import Post, Category, Author, Tag, Comment

admin = Bottle()


@admin.route('/')
@authenticate
def admin_index():
    post_count = Post.select().count()
    comm_count = Comment.select().count()
    tag_count = Tag.select().count()
    cate_count = Category.select().count()
    author = Author.get(id=1)
    posts = Post.select().paginate(1, 5)
    comments = Comment.select().order_by(('published', 'desc')).paginate(1, 5)
    return template('admin/index.html', posts=posts, comments=comments,
                    post_count=post_count, comm_count=comm_count,
                    tag_count=tag_count, cate_count=cate_count, author=author)


@admin.route('/post')
@authenticate
def admin_post():
    posts = Post.select().paginate(1, 50)
    return template('admin/posts.html', posts=posts)


@admin.route('/comment')
@authenticate
def admin_comment():
    comments = Comment.select().order_by(('published', 'desc')).paginate(1, 50)
    return template('admin/comments.html', comments=comments)


@admin.route('/settings', method='GET')
@authenticate
def admin_settings():
    author = Author.get(id=1)
    return template('admin/settings.html', author=author)


@admin.route('/changepass', method='POST')
@authenticate
def admin_changepass():
    oldpass = request.forms.get('oldpass').decode('utf-8')
    pass1 = request.forms.get('newpass').decode('utf-8')
    pass2 = request.forms.get('newpass2').decode('utf-8')
    try:
        user = Author.get(id=1)
    except Author.DoesNotExist:
        redirect('/admin')
    enpass = user.password
    if (is_password(oldpass, enpass) and pass1 == pass2):
        newpass = hexpassword(pass1)
        Author.update(password=newpass).where(id=1).execute()
        redirect('/admin')
    redirect('/admin/settings')
