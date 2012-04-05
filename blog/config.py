#!/usr/bin/env python
# -*- coding: utf-8 -*-

DBTYPE = "mysql"  #mysql or sqlite

SQLite = r"/home/blog/blog.db"  #if database is sqlite

MySQL = {"host": "localhost",
         "dbname":"blog",   #Database name
         "user": "root",    #User
         "passwd": "xxxxxxx", #MySQL Password
         "use_unicode": True, 
         "charset": "utf8"
        }

SECRET = "&29384934857&^&%^Knh72t$rBu8-5lKJumqSKEK-H/K6*0uL" 

PICKY_DIR = r"/home/blog/picky/" #Picky dir

STATIC_DIR = r"/home/blog" # Static dir
