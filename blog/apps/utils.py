#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from hashlib import md5, sha1
import random
import functools
from bottle import jinja2_template, request, redirect

import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
import markdown

from models import Author
from config import SECRET, STATIC_DIR


def codeblock(text):
    pattern = re.compile(
        r'\[code:(.+?)\](.+?)\[/code\]', re.S)
    formatter = HtmlFormatter(noclasses=False)

    def repl(m):
        try:
            lexer = get_lexer_by_name(m.group(1))
        except ValueError:
            lexer = TextLexer()
        code = highlight(m.group(2), lexer, formatter)
        code = code.replace('\n\n', '\n&nbsp;\n').replace('\n', '<br />')
        return '\n\n<div class="code">%s</div>\n\n' % code
    return pattern.sub(repl, text)


def to_markdown(text):
    text = codeblock(text)
    md = markdown.Markdown()
    return md.convert(text)


def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    return value


def hexpassword(password):
    """
    加密密码
    """
    seed = "1234567890abcdefghijklmnopqrstuvwxyz \
           ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    enpass = sha1(sha1((salt + password).encode('utf-8')).hexdigest(). \
             encode('utf-8')).hexdigest()

    return str(salt) + '$' + str(enpass)


def is_password(passwd, enpass):
    salt = enpass[:8]
    password = sha1(sha1((salt + passwd).encode('utf-8')).hexdigest(). \
               encode('utf-8')).hexdigest()
    p = str(salt) + '$' + str(password)
    return p == enpass


def get_auth_user():
    userid = request.get_cookie("user", secret=SECRET)
    try:
        user = Author.get(id=userid)
    except Author.DoesNotExist:
        return None
    return user


def authenticate(handler):
    def _check_auth(*args, **kwargs):
        user = get_auth_user()
        if user:
            return handler(*args, **kwargs)
        redirect('/')
    return _check_auth


def is_admin(user):
    user = get_auth_user()
    if user:
        return True
    else:
        return False


def static_url(name):
    f = os.path.join(STATIC_DIR, name)
    url = '/'
    if not os.path.exists(f):
        return os.path.join(url, name)
    f = open(f, 'rb')
    stat = md5(f.read()).hexdigest()
    return os.path.join(url, name) + '?v=' + stat[:5]


def more_split(text):
    text = text.split("<!--more-->")
    return text[0]


def escape(s):
    if s is None:
        return ''
    elif hasattr(s, '__html__'):
        return s.__html__()
    elif not isinstance(s, basestring):
        s = unicode(s)
    s = s.replace('&', '&amp;').replace('<', '&lt;'). \
        replace('>', '&gt;').replace('"', "&quot;"). \
        replace(u"'", u"&#39;").replace('\n', "<br />")
    return s


def aunquote(text):
    text = text.replace(u"&lt;a", u'<a')
    text = text.replace(u"href=&quot;", u'href="')
    text = text.replace(u"&quot;&gt;", u'">')
    text = text.replace(u"&lt;/a&gt;", u"</a>")
    text = text.replace(u"&lt;pre&gt;", u"<pre>")
    text = text.replace(u"&lt;/pre&gt;", u"</pre>")
    return text


def archives_list(posts):
    years = list(set([post.published.year for post in posts]))
    years.sort(reverse=True)
    for year in years:
        year_posts = [post for post in posts if post.published.year == year]
        yield (year, year_posts)


settings = dict(
          filters={'static_url': static_url, 'more_split': more_split,
                     'unquote': aunquote, "escape": escape},
          tests={"admin": is_admin},
          )

template = functools.partial(jinja2_template, template_settings=settings)
