import time,sys
from threading import Thread
class parse:
    def __init__(
        self,url,type_url='text',login='',Parsing='',label={},write='',\
        next_url='',page=[False],clean=False,write_SQL={},texting=False, \
        status="None",Thread_num=1,sem=5,cpu_count=0 ):
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
        self.files,self.url,self.times = [],'',1
        self.first_url,self.type_url,self.login,self.Parsing,self.label = url,type_url,login,Parsing,label
        self.write,self.next_url,self.page,self.clean,self.write_SQL = write,next_url,page,clean,write_SQL
        self.texting,self.status,self.Thread_num,self.sem,self.cpu_count = texting,status,Thread_num,sem,cpu_count
        self.judge()
    def judge(self):
        '''  
        检查传参格式是否正常
        :param type_url,login,Parsing,label,write,
               next_url,page,clean,write_SQL,status,Thread_num,
               sem,cpu_count
        :return True or False
        '''
        if not isinstance(self.type_url, str):
            raise ValueError('type_url is str')
        if not isinstance(self.login, str):
            raise ValueError('login is str')
        if not isinstance(self.Parsing, str):
            raise ValueError('Parsing is str')
        if not isinstance(self.label, dict):
            raise ValueError('label is dict')
        if not isinstance(self.write, str):
            raise ValueError('write is str')
        if not isinstance(self.next_url, str):
            raise ValueError('next_url is str')
        if not isinstance(self.page, list):
            raise ValueError('page is list')
        if not isinstance(self.clean, bool):
            raise ValueError('clean is bool')
        if not isinstance(self.write_SQL, dict):
            raise ValueError('write_SQL is dict')
        if not isinstance(self.status, str):
            raise ValueError('status is str')
        if not isinstance(self.Thread_num, int):
            raise ValueError('Thread_num is int')
        if not isinstance(self.sem,int):
            raise ValueError("sem is int")
        if not isinstance(self.cpu_count,int):
            raise ValueError("cpu_count is int")
    def run(self):
        program = self.threads()
        if self.texting:
            while True:
                try:
                    if not program.is_alive():
                        self.times += 1
                        self.threads()
                        if self.times == 5:
                            time.sleep(2)
                            sys.exit(0)
                    time.sleep(3)
                except:break
        return program
    def threads(self):
        program = MyThread(self.status,self.first_url,self.type_url,self.login,self.Parsing,self.label,\
            self.write,self.next_url,self.page,self.clean,self.write_SQL,self.Thread_num,self.sem,self.cpu_count)
        program.start()
        program.join()
        return program.get_result()
class MyThread(Thread):
    def __init__(self,status,first_url,type_url,login,Parsing,label,\
            write,next_url,page,clean,write_SQL,Thread_num,sem,cpu_count):
        super(MyThread,self).__init__()
        self.status = status
        self.url,self.type_url,self.login,self.Parsing,self.label,self.write,self.next_url,self.page,self.clean,self.write_SQL,self.Thread_num,self.sem,self.cpu_count = first_url,type_url,login,Parsing,label,write,next_url,page,clean,write_SQL,Thread_num,sem,cpu_count
    def run(self):
        if self.status.lower() == "none":
            from . import Thread_run
            self.result = Thread_run.ordinary(self.url,self.type_url,self.login,self.Parsing,self.label,self.write,self.next_url,self.page,self.clean,self.write_SQL).run()
        elif self.status.lower() == 'multiprocessing':
            from . import multiproces
            multiproces.mult(self.url,self.type_url,self.login,self.Parsing,self.label,self.write,self.clean,self.write_SQL,self.cpu_count).run()
        elif self.status.lower() == 'threads':
            from . import Threads_run
            Threads_run.Threads(self.url,self.type_url,self.login,self.Parsing,self.label,self.write,self.clean,self.write_SQL,self.Thread_num).run()
        elif self.status.lower() == "aiohttp":
            from . import asyn_run
            self.result = asyn_run.asyn_http(self.url,self.type_url,self.login,self.Parsing,self.label,self.write,self.clean,self.write_SQL,self.sem,self.Thread_num).run()
        elif self.status.lower() == "between":
            from . import double
            self.result = double.double(self.url,self.type_url,self.login,self.Parsing,self.label,self.write,self.clean,self.write_SQL,self.cpu_count,self.sem).run()
        else:
            raise ValueError("status's parameter error !")
    def get_result(self):
        try:return self.result
        except:return None