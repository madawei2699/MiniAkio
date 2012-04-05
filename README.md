### 关于MiniAkio

MiniAkio是使用Python开发的一个简单的博客系统，使用了Bottle、Jinja2，并采用Markdown格式写作。由于开发一个博客系统是重复造轮子的事，因此这个博客系统主要是用做参考，可以供学习Bottle的参考，当然，是可以运行的，但安装比较麻烦。

### 使用MiniAkio

依赖的第三方库包括下面的这些：
>1. [Bottle][1]
2. [Jinja2][2]
3. [MarkDown][3]
4. [Pygments][4]

以上可以pip安装之。支持MySQL、SQLite数据库，使用时需要导入Tools中的sql文件，因为缺少很多设置的功能，因此你只能在数据库中完成了。

如何运行MiniAkio，因为采用Bottle框架，所以支持Bottle的都可以，可以参考[Bottle的运行方式][5]。

### 更多说明

关于MiniAkio的更多说明可以参考[我的博客][6]。

[1]:http://bottlepy.org/docs/dev/
[2]:http://jinja.pocoo.org/docs/
[3]:http://pypi.python.org/pypi/Markdown
[4]:http://pygments.org/
[5]:http://bottlepy.org/docs/dev/tutorial.html#deployment
[6]:http://serholiu.com/picky/MiniAkio
