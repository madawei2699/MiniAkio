#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from bottle import Bottle, request, redirect, abort, response
from utils import template, authenticate, to_markdown, escape
from models import Post, Category, Tag, Comment

blog = Bottle()


@blog.route('/')
def index():
    posts = Post.select().paginate(1, 5)
    return template('index.html', posts=posts, page=1)


#Redirect 301............
@blog.route('/<slug>/')
def redirect_post(slug='test-post'):
    redirect("/%s" % slug, code=301)


@blog.route('/tag/<tag>/')
def redirect_tag(tag):
    redirect("/tag/%s" % tag, code=301)


@blog.route('/page/<num:int>/')
def redirect_page(num):
    redirect("/page/%d" % int(num), code=301)


@blog.error(404)
def error404(error):
    return template('e404.html')


@blog.route('/<slug>')
def single_post(slug='test-post'):
    try:
        post = Post.get(slug=slug)
    except Post.DoesNotExist:
        abort(404)
    return template('post.html', post=post)


@blog.route('/page/<num:int>')
def page_post(num):
    if num < 1:
        abort(404)
    posts = Post.select().paginate(num, 5)
    post_count = posts.count()
    pages = (post_count - 1) / 5 + 1
    return template('index.html', posts=posts, page=num, pages=pages)


@blog.route('/tag/<tag>')
def tag_archive(tag):
    tag = tag.decode('utf-8')
    try:
        tags = Tag.select().where(name=tag)
    except Tag.DoesNotExist:
        abort(404)
    postids = [_tag.post_id for _tag in tags]
    posts = Post.select().where(id__in=postids)
    count = posts.count()
    return template('archive.html', posts=posts, name=tag,
                    type="tag", count=count)


@blog.route('/category/<category>')
def category_archive(category):
    category = category.decode('utf-8')
    try:
        category = Category.get(slug=category)
    except Category.DoesNotExist:
        abort(404)
    posts = category.posts
    count = posts.count()
    return template('archive.html', posts=posts, name=category.name,
                    type="category", count=count)


@blog.route('/blog/all')
def blog_achive():
    posts = Post.select()
    from utils import archives_list
    count = posts.count()
    return template('archives.html', posts=posts, count=count,
                    archives_list=archives_list)


@blog.route('/search/all')
def blog_search():
    return template('search.html')


@blog.route('/blog/feed')
def blog_feed():
    def _format_date(dt):
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()],
            dt.day,
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month - 1],
            dt.year, dt.hour, dt.minute, dt.second)
    posts = Post.select().paginate(1, 10)
    response.content_type = 'application/rss+xml; charset=UTF-8'
    return template('feed.xml', posts=posts, format=_format_date)


@blog.route('/post/new', method='GET')
@authenticate
def get_new_post():
    category = Category.select()
    return template("admin/newpost.html", category=category)


@blog.route('/post/new', method='POST')
@authenticate
def post_new_post():
    title = request.forms.get('title').decode('utf-8')
    slug = request.forms.get('slug').decode('utf-8')
    post = request.forms.get('post')
    tags = request.forms.get('tags').decode('utf-8')
    category = request.forms.get('category').decode('utf-8')
    post_type = request.forms.get('postype')
    set_time = request.forms.get('setime')
    if set_time != '1':
        t = [int(tt) for tt in set_time.split('-')]
        d = datetime.datetime(*t)
        published = d
    else:
        published = datetime.datetime.now()

    if post_type == 'HTML':
        is_html = 1
        content = post.decode('utf-8')
        markdown = u'html'
    else:
        is_html = 0
        markdown = post.decode('utf-8')
        content = to_markdown(markdown)
    category = Category.get(name=category)
    post = Post.create(title=title, slug=slug.strip(), content=content,
                       markdown=markdown, tags=tags, category=category,
                       is_html=is_html, published=published, comm_count=0)
    for tag in post.tags_list():
        Tag.create(name=tag.strip(), post_id=post.id)
    redirect("/%s" % slug)


@blog.route('/post/update/<id:int>', method='GET')
@authenticate
def get_update_post(id):
    category = Category.select()
    try:
        post = Post.get(id=id)
    except Post.DoesNotExist:
        abort(404)
    return template("admin/update.html", post=post, category=category)


@blog.route('/post/update/<id:int>', method='POST')
@authenticate
def post_update_post(id):
    postid = request.forms.get('postid')
    title = request.forms.get('title').decode('utf-8')
    slug = request.forms.get('slug').decode('utf-8')
    post = request.forms.get('post')
    tags = request.forms.get('tags').decode('utf-8')
    category = request.forms.get('category').decode('utf-8')
    post_type = request.forms.get('postype')
    if post_type == 'HTML':
        is_html = 1
        content = post.decode('utf-8')
        markdown = u'html'
    else:
        is_html = 0
        markdown = post.decode('utf-8')
        content = to_markdown(markdown)
    category = Category.get(name=category)
    Post.update(title=title, slug=slug, content=content, markdown=markdown,
                tags=tags, category=category,
                is_html=is_html).where(id=postid).execute()
    tag_list = set(tags.split(","))
    for tag in tag_list:
        try:
            Tag.get(name=tag, post_id=postid)
        except Post.DoesNotExist:
            Tag.create(name=tag, post_id=postid)
    redirect("/%s" % slug)


@blog.route('/post/del/<id:int>')
@authenticate
def post_del_post(id):
    Post.delete().where(id=id).execute()
    redirect("/")


@blog.route('/comment/new', method='POST')
def post_new_comment():
    postid = request.forms.get('postid')
    name = request.forms.get('name').decode('utf-8')
    email = request.forms.get('email').decode('utf-8')
    url = request.forms.get('url').decode('utf-8')
    content = request.forms.get('content').decode('utf-8')
    parent = request.forms.get('parentid')
    check = request.forms.get('check')
    if check != "123456":
        post = Post.get(id=postid)
        redirect("/%s" % post.slug)

    post = Post.get(id=postid)
    post.comm_count = post.comm_count + 1
    comment = Comment.create(post=post, author=escape(name),
                             email=escape(email), url=escape(url),
                             content=escape(content), parent=parent,
                             published=datetime.datetime.now())
    post.save()
    redirect("/%s#comment-%s" % (post.slug, comment.id))


@blog.route('/comment/del/<id:int>')
@authenticate
def del_comment(id):
    comment = Comment.get(id=id)
    comment.post.comm_count = comment.post.comm_count - 1
    comment.post.save()
    Comment.delete().where(id=id).execute()
    redirect("/admin/comment")
