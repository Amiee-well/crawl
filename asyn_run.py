import random
import aiohttp
import asyncio
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
class asyn_http:
    def __init__(self,url,type_url,login,Parsing,label,write,clean,write_SQL,sem,Thread_num):
        if not isinstance(url, list):
            raise ValueError('url is list')
        self.title,self.files = label.keys(),[]
        self.url,self.type_url,self.login,self.Parsing = url,type_url,login,Parsing
        self.label,self.write,self.clean,self.write_SQL = label,write,clean,write_SQL
        self.Thread_num = Thread_num
        #self.sem = asyncio.Semaphore(sem)
        self.headers = {'User-Agent': random.choice(user_agent)}
    def run(self):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        q = asyncio.Queue()
        [q.put_nowait(url) for url in self.url]
        tasks = [self.handle_tasks(task_id,q,) for task_id in range(self.Thread_num)]
        result = loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        return result
    async def handle_tasks(self, task_id, work_queue):
        while not work_queue.empty():
            current_url = await work_queue.get()
            try:
                return await self.get_results(current_url)
            except:
                import logging
                logging.exception('Error for {}'.format(current_url), exc_info=True)
    async def get_body(self,url):
        #with(await self.sem):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as resp:
                assert resp.status == 200
                self.text = await resp.read()
                print("[Info] : Response is ok , Get the source code")
    async def get_results(self, url):
        await self.get_body(url)
        return self.parse_results()
    def parse_results(self):
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
    def parsing(self):
        if self.Parsing.lower() == 're':
            import re
            texts = {}
            try:
                for title in self.title:
                    label = self.label[title]
                    label_text = re.findall(r'{}'.format(label[0]),self.text,'re.S')
                    if len(label)==2:label_text = list(map(label[1], label_text))
                    texts[title] = label_text
                print('[Info] : parsing is finish')
            except Exception as err:
                raise err
            return texts
        elif self.Parsing.lower() == "xpath":
            from lxml import etree
            texts = {}
            try:
                dom = etree.HTML(self.text)
                for title in self.title:
                    label = self.label[title]
                    label_text = dom.xpath(r'{}'.format(label[0]))
                    if len(label)==2:label_text = list(map(label[1], label_text))
                    texts[title] = label_text
                print('[Info] : parsing is finish')
            except Exception as err:
                raise err
            return texts
        elif self.Parsing.lower() == "bs4":
            from bs4 import BeautifulSoup
            texts = {}
            try:
                bs = BeautifulSoup(self.text,"html.parser")
                for title in self.title:
                    label = self.label[title]
                    label_text = bs.select(label[0])[0].get_text()
                    if len(label)==2:label_text = list(map(label[1], label_text))
                    texts[title] = label_text
                print('[Info] : parsing is finish')
            except Exception as err:
                raise err
            return texts
    def Handling_saving(self):
        if self.clean:
            from cleancc import clean
            try:clean.word_all(self.files)
            except:print('[warning : Cleaning only allows strings ! ]')
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
            print('[Info] : write txt finish')
        elif self.write.split('.')[-1] == 'json':
            self.write_json(texts)
            print('[Info] : write json finish')
        elif self.write.split('.')[-1] == 'pkl':
            self.write_pkl(texts)
            print('[Info] : write pkl finish')
        elif self.write.split('.')[-1] == 'csv':
            self.write_csv(texts)
            print('[Info] : write csv finish')
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
