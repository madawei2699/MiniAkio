PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE author (id INTEGER NOT NULL PRIMARY KEY, username VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL, email VARCHAR(30) NOT NULL, join_date DATETIME NOT NULL);

/*在下面的SQL语句设置帐号相关信息，请注意，第三个字段不要更改，字段代表意思请参考上一条语句*/
INSERT INTO "author" VALUES(1,'admin','FU$H289o$cbeb8bc34cf09933fed8f2bd520d0933d8562696','s@q.com','2011-12-14 21:41:51');

CREATE TABLE category (id INTEGER NOT NULL PRIMARY KEY, name VARCHAR(50) NOT NULL, slug VARCHAR(50) NOT NULL);

/*添加分类,可以添加多个，请按照下面注释语句格式，其中第一个是主键，要逐次递增，并去掉注释*/

--INSERT INTO "category" VALUES(1,'Web','web');
--INSERT INTO "category" VALUES(2,'Web','web');

CREATE TABLE post (id INTEGER NOT NULL PRIMARY KEY, title VARCHAR(100) NOT NULL, slug VARCHAR(100) NOT NULL, content TEXT NOT NULL, markdown TEXT NOT NULL, tags VARCHAR(255) NOT NULL, category_id INTEGER NOT NULL REFERENCES category (id), published DATETIME NOT NULL, is_html INTEGER NOT NULL, comm_count INTEGER NOT NULL);
CREATE TABLE tag (id INTEGER NOT NULL PRIMARY KEY, name VARCHAR(50) NOT NULL, post_id INTEGER NOT NULL);
CREATE TABLE comment (id INTEGER NOT NULL PRIMARY KEY, post_id INTEGER NOT NULL REFERENCES post (id), author VARCHAR(50) NOT NULL, email VARCHAR(50) NOT NULL, url VARCHAR(100) NOT NULL, content TEXT NOT NULL, published DATETIME NOT NULL, parent INTEGER NOT NULL);
CREATE UNIQUE INDEX author_id ON author(id);
CREATE UNIQUE INDEX category_id ON category(id);
CREATE UNIQUE INDEX post_id ON post(id);
CREATE INDEX post_category_id ON post(category_id);
CREATE INDEX post_slug ON post(slug);
CREATE UNIQUE INDEX tag_id ON tag(id);
CREATE UNIQUE INDEX comment_id ON comment(id);
CREATE INDEX comment_post_id ON comment(post_id);
COMMIT;
