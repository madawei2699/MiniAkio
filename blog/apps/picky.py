#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bottle import Bottle, redirect, abort, request
from utils import template, to_markdown, to_unicode, authenticate

from config import PICKY_DIR

picky = Bottle()


@picky.error(404)
def error404(error):
    return template('e404.html')


@picky.route('/upload', method='POST')
@authenticate
def upload_picky():
    picky = request.files.picky
    name = picky.filename
    file_type = name.split('.')[1]
    if picky.file and (file_type == 'md'):
        fin = picky.file.read()
        fout = open(PICKY_DIR + name, 'w')
        fout.write(fin)
        fout.close()
        slug = name.split('.')[0]
        redirect("/picky/%s" % slug)
    redirect("/admin/settings")


@picky.route('/<slug>')
def single_picky(slug='test'):
    try:
        f = open(PICKY_DIR + slug + '.md')
    except IOError:
        abort(404)
    picky = f.read()
    f.close()
    meta_regex = re.compile(
            r"^\s*(?:-|=){3,}\s*\n((?:.|\n)+?)\n\s*(?:-|=){3,}\s*\n*",
            re.MULTILINE
        )
    match = re.match(meta_regex, picky)
    if not match:
        abort(404)
    metas = match.group(1)
    title = None
    date = None
    meta = metas.split("\n")
    try:
        title = meta[0].split("=>")[1]
    except IndexError:
        title = meta[0].split("=>")[0]
    try:
        date = meta[1].split("=>")[1]
    except IndexError:
        date = meta[1].split("=>")[0]
    cont = to_unicode(picky[match.end():])
    content = to_markdown(cont)
    return template('picky.html', content=content, title=to_unicode(title),
                                 date=to_unicode(date), slug=slug)
