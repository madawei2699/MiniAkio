#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hashlib import md5
from libs.peewee import *
from config import DBTYPE, SQLite, MySQL

if DBTYPE is "sqlite":
    database = SqliteDatabase(SQLite)
elif DBTYPE is "mysql":
    database = MySQLDatabase(MySQL["dbname"], **MySQL)


class BaseModel(Model):
    class Meta:
        database = database


class Author(BaseModel):
    username = CharField(max_length=50)
    password = CharField(max_length=50)
    email = CharField(max_length=30)
    join_date = DateTimeField()

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(),
                 size)


class Category(BaseModel):
    name = CharField(max_length=50)
    slug = CharField(max_length=50)


class Post(BaseModel):
    title = CharField(max_length=100)
    slug = CharField(db_index=True, max_length=100)
    content = TextField()
    markdown = TextField()
    tags = CharField()
    category = ForeignKeyField(Category, related_name='posts')
    published = DateTimeField()
    is_html = IntegerField()
    comm_count = IntegerField()

    def tags_list(self):
        tags = self.tags.split(",")
        return set(tags)

    @property
    def next_post(self):
        next = self.id + 1
        count = Post.select().count()
        while(True):
            try:
                post = Post.get(id=next)
                return {"slug": post.slug, "title": post.title}
            except Post.DoesNotExist:
                if next >= count:
                    break
                else:
                    next = next + 1
        return None

    @property
    def prev_post(self):
        next = self.id - 1
        while(True):
            try:
                post = Post.get(id=next)
                return {"slug": post.slug, "title": post.title}
            except Post.DoesNotExist:
                if next == 0:
                    break
                else:
                    next = next - 1
        return None

    class Meta:
        ordering = (('published', 'DESC'),)


class Tag(BaseModel):
    name = CharField(max_length=50)
    post_id = IntegerField()


class Comment(BaseModel):
    post = ForeignKeyField(Post, related_name='comments')
    author = CharField(max_length=50)
    email = CharField(max_length=50)
    url = CharField(max_length=100)
    content = TextField()
    published = DateTimeField()
    parent = IntegerField()

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(),
                 size)

    def get_url(self):
        return '/%s#comment-%s' % (self.post.slug, self.id)
