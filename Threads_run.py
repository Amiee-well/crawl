from . import ip_proxy
import random,os,requests
from time import sleep
from threading import Thread

user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
]
class Threads:
    def __init__(
        self,url,type_url='text',login='',Parsing='',label={},write='',\
        clean=False,write_SQL={},Thread_num=1 \
            ):
        '''
        多线程爬虫程序执行
        :param url:即将请求的url地址,仅支持get请求
        :param type_url:请求url后返回格式,支持text和json格式返回
        :param login:模拟网站登陆,保存登陆信息
        :param Parsing:爬虫方式,支持re、xpath以及bs4方法
        :param label:选择器内容,字典格式保存,
                     字典值为列表格式,第一个参数为选择器,第二个参数为转换类型
                     第一个参数必填,第二个参数默认str类型
        :param write:是否写入文件,支持txt格式、csv格式、json格式以及pkl格式,默认否,
        :param clean:是否进行简单类型数据清洗,默认否
        :param write_sql:是否写入数据库,默认否
                         'host'默认为'localhost','post'默认'3306','user'默认'root',
                         'password':'密码','db':'数据库','table':'数据表',
                         检测表是否存在,若不存在则创建,若存在则直接插入.
        :param Thread_num:即将启动多线程个数,默认为1单线程
        :return True
        '''
        if not isinstance(url, list):
            raise ValueError('url is list')
        self.files,self.url = [],''
        self.title = label.keys()
        self.first_url,self.type_url,self.login,self.Parsing,self.label = url,type_url,login,Parsing,label
        self.write,self.clean,self.write_SQL,self.Thread_num = write,clean,write_SQL,Thread_num
        self.headers = {'User-Agent': random.choice(user_agent)}
    def parse_login(self):
        '''
        爬虫登陆阶段登陆处理
        该六种为二维码登陆,扫码即可登陆后
        session信息保存到本地读取
        支持QQ群、QQ空间、QQ安全中心、淘宝、京东和斗鱼登陆
        :param login
        :return session
        '''
        from DecryptLogin import login
        lg = login.Login()
        if self.login.lower() == 'qqqun':
            if self.first_url[0].split('.com')[0][-6:] == 'qun.qq':
                _, self.session = lg.QQQun()
            else:raise ValueError('The url box does not match the login')
        elif self.login.lower() == 'qqzone':
            if self.first_url[0].split('.com')[0][-9:] == '.qzone.qq':
                _, self.session = lg.QQZone()
            else:raise ValueError('The url box does not match the login')
        elif self.login.lower() == 'qqid':
            if self.first_url[0].split('.com')[0][-6:] == '.id.qq':
                _, self.session = lg.QQId()
            else:raise ValueError('The url box does not match the login')
        elif self.login.lower() == 'taobao':
            if self.first_url[0].split('.com')[0][-7:] == '.taobao':
                _, self.session = lg.taobao()
            else:raise ValueError('The url box does not match the login')
        elif self.login.lower() == 'jingdong':
            if self.first_url[0].split('.com')[0][-3:] == '.jd':
                _, self.session = lg.jingdong()
            else:raise ValueError('The url box does not match the login')
        elif self.login.lower() == 'douyu':
            if self.first_url[0].split('.com')[0][-6:] == '.douyu':
                _, self.session = lg.douyu()
            else:raise ValueError('The url box does not match the login')
        else:
            raise ValueError('Login box input error')
    def run(self):
        '''
        多线程判断能否运行
        每个线程平分url个数是否为整数,必须被平分
        :param
        :return
        '''
        if len(self.first_url)%self.Thread_num == 0:
            self.Thread_()
        else:
            raise ValueError("Thread_num's parameter error !")
    def Thread_(self):
        '''
        多线程启动
        循环启动多线程,每个线程平分url个数
        :param num:整除后结果判断每个线程几个url
        :return
        '''
        num = len(self.first_url)//self.Thread_num
        for Thread_soon in range(self.Thread_num):
            running = Thread(target=self.formal_run,args=(list(self.first_url[num*Thread_soon:num*(Thread_soon+1)])))
            running.start()
    def formal_run(self,*urls):
        '''
        程序运行
        :param urls:准备访问的url地址群体
        :return
        '''
        for url in urls:
            self.text = self.request(url)
            if len(self.Parsing):
                parm_texts = self.parsing()
                self.files.append(parm_texts)
                if not len(self.write):
                    return parm_texts
                if len(self.write_SQL):
                    from . import write_SQL
                    write_SQL.write_sql(self.write_SQL,self.label,self.files)
            else:return self.text
            if len(self.write) or self.clean:
                return self.Handling_saving()
    def request(self,url,*proxy):
        '''
        爬虫初期访问阶段
        url开始访问, 访问出现错误则使用代理访问
        :param url:请求访问的url地址
        :return text:url页面解析源代码
        '''
        self.times = 0
        if type(url) == tuple:url = url[0]
        try:
            if self.login:
                import pickle
                if os.path.isfile(self.login+'_session.pkl'):
                    self.session = pickle.load(open(self.login+'_session.pkl', 'rb'))
                else:
                    self.parse_login()
                    f = open(self.login+'_session.pkl', 'wb')
                    pickle.dump(self.session, f)
                    f.close()
                html = self.session.get(url)
            else:
                if proxy:html = requests.get(url,headers = self.headers,proxies = proxy)
                else:html = requests.get(url,headers = self.headers)
            if html.status_code == 200:
                print("[Info] : Response is ok , Get the source code\n")
                try:self.ip_mode.stop_thread(self.ip_mode.__dict__["ip"])
                except:pass
                if self.type_url.lower() == 'text':
                    return html.text
                elif self.type_url.lower() == 'json':
                    return html.json
                else:
                    raise ValueError("type_url's parameter error")
        except Exception as err:
            print(err)
            self.times += 1
            self.ip_mode = Thread(target=ip_proxy.xici_proxy)
            self.ip_mode.start()
            print("[warning] : Response is err , Preparing to start agent\n")
            sleep(5)
            while True:
                if os.path.exists('ip.txt'):
                    with open('ip.txt','r') as ip:
                        self.ip_list = ip.read()
                    break
                else:sleep(5)
            self.ip_proxy()
    def ip_proxy(self):
        '''
        爬虫初期代理选择
        url访问失败,初步选择代理继续访问url
        :param 
        :return 
        '''
        ip_list = self.ip_list.split('\n')[:-1]
        ip_one = random.choice(ip_list)
        if self.times == 5:
            try:self.ip_mode.stop_thread(self.ip_mode.__dict__["ip"])
            except:pass
            raise EOFError('Visited more than five times')
        sleep(5)
        self.request(ip_one)
    def parsing(self):
        '''
        爬虫处理阶段
        判断解析方式,通过解析选择器解析url内容
        :param Parsing:选择器类型
        :param label:选择器内容
        :return texts:解析后的url返回结果
        '''
        if self.Parsing.lower() == 're':
            import re
            texts = {}
            for title in self.title:
                label = self.label[title]
                label_text = re.findall(r'{}'.format(label[0]),self.text,'re.S')
                if len(label)==2:label_text = list(map(label[1], label_text))
                texts[title] = label_text
            print('[Info] : parsing is finish\n')
            return texts
        if self.Parsing.lower() == 'xpath':
            from lxml import etree
            texts = {}
            dom = etree.HTML(self.text)
            for title in self.title:
                label = self.label[title]
                label_text = dom.xpath(r'{}'.format(label[0]))
                if len(label)==2:label_text = list(map(label[1], label_text))
                texts[title] = label_text
            print('[Info] : parsing is finish\n')
            return texts
        if self.Parsing.lower() == 'bs4':
            from bs4 import BeautifulSoup
            texts = {}
            bs = BeautifulSoup(self.text,"html.parser")
            for title in self.title:
                label = self.label[title]
                label_text = bs.select(label[0])[0].get_text()
                if len(label)==2:label_text = list(map(label[1], label_text))
                texts[title] = label_text
            print('[Info] : parsing is finish\n')
            return texts
    def Handling_saving(self):
        if self.clean:
            from cleancc import clean
            try:clean.word_all(self.files)
            except:print('[warning : Cleaning only allows strings ! ]\n')
        if len(self.write):
            self.write_ROM(self.files)
    def write_ROM(self,texts):
        '''
        判断写入位置函数
        :param texts:即将写入的文件
        :return function:写入函数
        '''
        if self.write.split('.')[-1] == 'txt':
            self.write_txt(texts)
            print('[Info] : write txt finish\n')
        elif self.write.split('.')[-1] == 'json':
            self.write_json(texts)
            print('[Info] : write json finish\n')
        elif self.write.split('.')[-1] == 'pkl':
            self.write_pkl(texts)
            print('[Info] : write pkl finish\n')
        elif self.write.split('.')[-1] == 'csv':
            self.write_csv(texts)
            print('[Info] : write csv finish\n')
        else:
            raise ValueError('[warning] : Incorrect access')
    def write_csv(self,texts):
        import csv
        with open(self.write, 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(self.title)
            for text in texts:
                csv_writer.writerow([text[value] for value in text.keys()])
    def write_txt(self,texts):
        '''
        写入txt文件
        :param texts:即将写入的文件
        :return txt:保存下的txt文件信息
        '''
        import json
        for text in texts:
            text = json.dumps(text, ensure_ascii=False)
            with open(self.write, 'a', encoding='utf-8') as f:
                f.write(text+'\n')
    def write_json(self,texts):
        '''
        写入json文件
        :param texts:即将写入的文件
        :return json:保存下的json文件信息
        '''
        import json
        for text in texts:
            text = json.dumps(text, indent=4)
            with open(self.write, 'a', encoding='utf-8') as f:
                f.write("{\n"+text+"\n}")
    def write_pkl(self,texts):
        '''
        写入pkl文件
        :param texts:即将写入的文件
        :return pkl:保存下的pkl文件信息
        '''
        import pickle
        for text in texts:
            with open(self.write, 'ab') as f:
                pickle.dump(text, f)