## 仅需一行代码写爬虫--simple_crawl

---

### simple_crawl
- 仅需一行代码即可达到爬虫效果
- 项目地址(欢迎star):[https://github.com/Amiee-well/crawl](https://github.com/Amiee-well/crawl)

### 使用方法
**pip install simple_crawl**
```python
from simple_crawl import request
request.parse(
	url=['https://www.douban.com/group/explore?start={}'.format(i) for i in range(0,180,30)],
        #login="taobao",
        type_url = "text",
        Parsing = 'xpath',
        label = {
            'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
            'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
            'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
            },
        write='result.txt',
        next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
        page=[True,"now_url.txt"],
        #clean=True,
        texting=True,
        status="aiohttp",
        Thread_num=3,
        cpu_count=1,
        sem=5,
        write_SQL={
            'host':'localhost',
            'post':'3306',
            'user':'root',
            'password':'123456',
            'db':'example',
            'table':'example'
            }
).run()
```
---
介绍一下crawl参数设置：

```python
'''
单行代码爬虫程序执行
:param status:启用爬虫类型,支持普通爬虫、多进程爬虫、多线程爬虫、异步爬虫、异步多进程爬虫,参数请参考文档
:param url:即将请求的url地址,仅支持get请求
:param type_url:请求url后返回格式,支持text和json格式返回
:param Thread_num:即将启动多线程个数,默认为1单线程
:param sem:协程信号量,控制协程数,防止爬的过快,默认为5
:param cpu_count:运行爬虫使用多进程cpu核数,默认为系统核数一半
:param login:模拟网站登陆,保存登陆信息
:param Parsing:爬虫方式,支持re、xpath以及bs4方法
:param texting:是否启用连续爬虫,爬虫程序异常报错后重新启动爬虫,
                       多次报错结束程序,默认否
:param label:选择器内容,字典格式保存,
                     字典值为列表格式,第一个参数为选择器,第二个参数为转换类型
                     第一个参数必填,第二个参数默认str类型
:param write:是否写入文件,支持txt格式、csv格式、json格式以及pkl格式,默认否
:param next_url:是否跨页爬虫,选择器内容使爬虫继续翻页爬虫
:param page:是否选择断续笔记接手下次爬虫处理,默认否
:param clean:是否进行简单类型数据清洗,默认否
:param write_sql:是否写入数据库,默认否
                         'host'默认为'localhost','post'默认'3306','user'默认'root',
                         'password':'密码','db':'数据库','table':'数据表',
                         检测库是否存在,若不存在则创建,若存在则直接插入,
                         检测表是否存在,若不存在则创建,若存在则直接插入
:return True
'''
```
---
## 介绍玩法
接下来介绍的均为调用第三方库的情况下运行：

```python
from simple_crawl import request
```

---
### 第一种玩法：输出源代码
调用requests库进行源代码请求。

特点：
请求失败则调用ip池处理重新请求访问，
出现五次失败默认网址输入错误。
支持text以及json字符串返回。默认text。

缺点：
暂时只能进行get请求，不支持post访问

：return text or json
```python
request.parse(
	url = "https://www.douban.com/group/explore",
	type_url = "text"
).run()
# return text
```
---
### 第二种玩法：模拟网站登陆并保存信息
调用DecryptLogin库请求登陆访问。

> ps：DecryptLogin库为大佬皮卡丘写的一个很不错的模拟网站登陆库，在此引用一下，因为单行爬虫原因不支持账号密码登陆，我将大佬写的二维码登陆使用过来了。再次感谢大佬开源
> 在此放出文档地址
> DecryptLogin库中文文档：[https://httpsgithubcomcharlespikachudecryptlogin.readthedocs.io/zh/latest/](https://httpsgithubcomcharlespikachudecryptlogin.readthedocs.io/zh/latest/)
> 

特点：
将DecryptLogin库中二维码继承到此库（非二次开发）
支持QQ群、QQ空间、QQ安全中心、淘宝、京东和斗鱼登陆（大佬登陆库中所有的二维码登陆）
保存session.pkl信息到本地方便下次登陆运行

缺点：
session.pkl登陆信息过时无法自动删除。
导致下次登陆疑似cookie无法正常登陆。

:return session

```python
request.parse(
	# 臭不要脸的推广一下我的店铺
	url="https://shop574805287.taobao.com/",
	login="taobao"
).run()
# return text
```
---
### 第三种玩法：爬取网站信息
爬虫库自然少不了爬虫的过程

特点：
支持re库，xpath解析以及bs4选择器。
爬取方法为字典格式。单方面输出。
字典键为保存的字段名称。
字典值为列表格式：第一个参数为选择器，第二个参数为转换类型。第一个参数必填，第二个参数默认str类型。

缺点：暂无（等待小伙伴们发现）

：return reptile_results
```python
request.parse(
	url='https://www.douban.com/group/explore',
	# 字符串格式,选择器方法。
    Parsing = 'xpath',
    # 字典格式,参数如上。
    label = {
        'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
        'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
        'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
        }
).run()
# return reptile_results（list）
```
---
### 第四种玩法：自由保存信息
目前版本支持保存txt、csv、json以及pkl四大主流文件。日后版本更新将发布更为全面的保存方法。

特点：
写入文件均为数据格式传入文件。
且输入格式规范方便阅读and省事。

缺点：
保存格式仅四种，
不方便用户之后读写操作。

：return file

```python
request.parse(
	url='https://www.douban.com/group/explore',
    Parsing = 'xpath',
    label = {
        'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
        'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
        'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
        },
    # 字符串格式,具体保存位置填写
    write='result.pkl'
).run()
# return file
```
---
### 第五种玩法：读取下一页 url 地址继续爬虫
这也是每个人都担心的问题，仅仅一行代码怎么可能翻页爬虫。这还真能做到哦~

特点：
继承之前的Parsing参数选择器选择方法。
在这里可读取到解析后的下一页 url 网址。
方可继续进行爬虫处理。方便用户使用。

缺点：
若爬虫时下一页 url 地址改变，便结束爬虫。
只能爬取所给 url 地址中的信息。
无法进行某一界面的多个网页爬取返回。
造成访问页面单一流失。

：return None

```python
request.parse(
	url='https://www.douban.com/group/explore',
    Parsing = 'xpath',
    label = {
        'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
        'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
        'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
        },
    write='result.pkl',
    # 字符串格式,根据Parsing方法继续请求下一页a中href
    next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
).run()
# return None 
```
---
### 第六种玩法：爬虫网页保存
听说过爬虫断续重连的朋友应该懂得这是个什么神仙操作。每次爬虫运行期间好好的，睡一觉醒来发现代码报错了。。。这就是个很难受的事，还不知道之前爬取到哪一页了，只能重新爬虫了啊！

特点：
持续输出断续笔记。
将此次爬虫的 url 地址保存到一个文本文档内部。
下次读取文本文档即可快速进行直接断掉的爬虫 url 地址继续爬取所需。

缺点：
读取内容不单一。
导致下次爬虫无法正确读取上次爬虫留下的痕迹。

：return url_file

```python
request.parse(
    url='https://www.douban.com/group/explore',
    type_url='text',
    #login='taobao',
    Parsing = 'xpath',
    label = {
        'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
        'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
        'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
        },
    write='result.pkl',
    next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
    # 第一个参数为是否需要断续笔记。
    # 第二个参数为断续笔记保存位置。
    page=[True,'url_page.txt']
).run()
# return url_file
```
### 第七种玩法：简单数据清洗
数据拿下后，直接保存到本地有些大佬可能觉得很辣鸡，连清洗都不清洗就存入本地了？那得拿到多少废数据脏数据。那么接下来介绍一下清洗参数。

特点：
本人曾写过一个底层数据清洗。
能将列表格式数据进行归分清洗。
主要内容请参考另一篇文章
如下连接：[数据清洗](https://blog.csdn.net/qq_45414559/article/details/105907938)

缺点：
数据清洗格式简单。
数据清洗内容单一。
无法完全做到绝对清洗。
有待改善。

：return keyword_list, value_list

```python
request.parse(
    url='https://www.douban.com/group/explore',
    Parsing = 'xpath',
    label = {
        'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
        'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
        'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
        },
    write='result.pkl',
    next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
    page=[True,'url_page.txt'],
    # bool类型,默认不清洗
    clean=True
).run()
```
---
### 第八种玩法：爬虫存入数据库
存到txt、存到csv、存到json、存到pkl，那也太low了吧。现在流行的数据库用不了么？那是不可能的。。

特点：
信息存入MySQL数据库。
可连接docker远程数据库。
数据库的库名可以不存在。
数据库的表名可以不存在。
根据之前传入字典键与值参数判断表类型。
自由建立数据表传入信息。

缺点：
仅支持MySQL数据库。

：return SQL

```python
request.parse(
    url='https://www.douban.com/group/explore',
    Parsing = 'xpath',
    label = {
        'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
        'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
        'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
        },
    write='result.pkl',
    next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
    page=[True,'url_page.txt'],
    clean=True,
    # 字典格式,
    # host可有可无,默认localhost
    # post可有可无,默认3306
    # user可有可无,默认root
    # password必要参数,数据库连接密码
    # db必要参数,数据库即将存入的库名
    # table必要参数,数据库即将存入的表名
    write_SQL={
        'host':'localhost',
        'post':'3306',
        'user':'root',
        'password':'123456',
        'db':'example',
        'table':'example'
        }
    ).run()
```
---
### 第九种玩法：重新启动爬虫
爬虫最让人厌烦的就是被一个不痛不痒的错误信息给终止爬虫了，比如意外的远程断开链接等低级非代码错误，报错之后还得重新启动断续爬虫，就显得很麻烦。我做了一期爬虫程序异常报错后重新启动爬虫，多次报错结束程序。

特点：
检测报错重新启动爬虫
无需手动处理错误信息

缺点：
无法收集子线程错误。

：return None

```python
request.parse(
	url=['https://www.douban.com/group/explore?start={}'.format(i) for i in range(0,180,30)],
        #login="taobao",
        type_url = "text",
        Parsing = 'xpath',
        label = {
            'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
            'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
            'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
            },
        write='result.txt',
        next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
        page=[True,"now_url.txt"],
        # texting 参数为是否启用连续爬虫
        # 爬虫程序异常报错后重新启动爬虫
        texting=True,
        ###
        write_SQL={
            'host':'localhost',
            'post':'3306',
            'user':'root',
            'password':'123456',
            'db':'example',
            'table':'example'
            }
).run()
```
---
### 第十种玩法：多线程爬虫
特点：
爬虫速度加快，
更好的利用了线程。

缺点：暂无

：return None

```python
request.parse(
	url=['https://www.douban.com/group/explore?start={}'.format(i) for i in range(0,180,30)],
        #login="taobao",
        type_url = "text",
        Parsing = 'xpath',
        label = {
            'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
            'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
            'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
            },
        write='result.txt',
        next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
        page=[True,"now_url.txt"],
        #clean=True,
        texting=True,
        # status="threads" 启用多线程爬虫
        # Thread_num 为线程数目,默认为1 单线程
        status="threads",
        Thread_num=3,
        ###
        write_SQL={
            'host':'localhost',
            'post':'3306',
            'user':'root',
            'password':'123456',
            'db':'example',
            'table':'example'
            }
).run()
```

---
### 第十一种玩法：多进程爬虫
特点：
爬虫速度加快，
更好的利用了进程。

缺点：暂无

：return None

```python
from simple_crawl import request
request.parse(
	url=['https://www.douban.com/group/explore?start={}'.format(i) for i in range(0,180,30)],
        #login="taobao",
        type_url = "text",
        Parsing = 'xpath',
        label = {
            'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
            'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
            'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
            },
        write='result.txt',
        next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
        page=[True,"now_url.txt"],
        #clean=True,
        texting=True,
        # status="multiprocessing" 启用多进程爬虫
        # cpu_count 为启动代码核心数,默认为系统核数一半
        status="multiprocessing",
        cpu_count=2,
        ###
        write_SQL={
            'host':'localhost',
            'post':'3306',
            'user':'root',
            'password':'123456',
            'db':'example',
            'table':'example'
            }
).run()
```

---
### 第十二种玩法：异步多线程爬虫
特点：
爬虫速度加快，
异步使得爬虫无等待时间，
同时使用多线程速度明显加快。

缺点：暂无

：return None

```python
from simple_crawl import request
request.parse(
	url=['https://www.douban.com/group/explore?start={}'.format(i) for i in range(0,180,30)],
        #login="taobao",
        type_url = "text",
        Parsing = 'xpath',
        label = {
            'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
            'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
            'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
            },
        write='result.txt',
        next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
        page=[True,"now_url.txt"],
        #clean=True,
        texting=True,
        # sem 参数为异步引擎数目,默认为5
        # 其他参数同上
        status="aiohttp",
        Thread_num=3,
        sem=5,
        ###
        write_SQL={
            'host':'localhost',
            'post':'3306',
            'user':'root',
            'password':'123456',
            'db':'example',
            'table':'example'
            }
).run()
```

---
### 第十三种玩法：异步多进程爬虫
特点：
爬虫速度加快，
异步使得爬虫无等待时间，
同时使用多进程速度明显加快。

缺点：暂无

：return None

```python
from simple_crawl import request
request.parse(
	url=['https://www.douban.com/group/explore?start={}'.format(i) for i in range(0,180,30)],
        #login="taobao",
        type_url = "text",
        Parsing = 'xpath',
        label = {
            'url':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/@href',str],
            'name':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/h3/a/text()',str],
            'Author':['//*[@id="content"]/div/div[1]/div[1]/div[1]/div[2]/div[2]/span[1]/a/text()',str]
            },
        write='result.txt',
        next_url='//*[@id="content"]/div/div[1]/div[2]/span[4]/a/@href',
        page=[True,"now_url.txt"],
        #clean=True,
        texting=True,
        # 参数如上
        status="between",
        cpu_count=1,
        sem=5,
        ###
        write_SQL={
            'host':'localhost',
            'post':'3306',
            'user':'root',
            'password':'123456',
            'db':'example',
            'table':'example'
            }
).run()

```

---
### 功能介绍完毕🤞

### 最后还是希望你们能给我点一波小小的关注。
### 奉上自己诚挚的爱心💖
