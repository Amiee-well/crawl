import random
from threading import Thread
import requests
from bs4 import BeautifulSoup
class xici_proxy:
    proxies = []
    index = -1
    def __init__(self):
        self.ip = Thread(target=self.getProxyIp)
        self.ip.start()
    def getOneAvailableProxy(self):
        global proxies
        if len(proxies) == 0:
            proxies = self.fetchAvalableProxyIpList()
        global index
        if (index < 0):
            index = random.randint(0, len(proxies) - 1)
        return proxies[index]
    def setTheProxyInavalid(self):
        global index
        index = -1
    def fetchAvalableProxyIpList(self):
        proxies = []
        for proxy in self.getProxyIp():
            proxies.append({'http': proxy})
        return proxies
    def _requestUrl(self,index):
        src_url = 'http://www.xicidaili.com/nt/'
        url = src_url + str(index)
        if index == 0:
            url = src_url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        }
        response = requests.get(url, headers=headers)
        return response.text
    def parseProxyIpList(self,content):
        list = []
        soup = BeautifulSoup(content, 'html.parser')
        ips = soup.findAll('tr')
        for x in range(1, len(ips)):
            tds = ips[x].findAll('td')
            ip_temp = 'http://' + tds[1].contents[0] + ':' + tds[2].contents[0]
            list.append(ip_temp)
        return list
    def filterValidProxyIp(self,list):
        validList = []
        for ip in list:
            if self.validateIp(ip):
                with open('ip.txt','a') as f:
                    f.write(ip+'\n')
                validList.append(ip)
        return validList
    def validateIp(self,proxy):
        proxy_temp = {"http": proxy}
        url = "http://ip.chinaz.com/getip.aspx"
        try:
            response = requests.get(url, proxies=proxy_temp, timeout=5)
            return response
        except Exception as e:
            return e
    def getProxyIp(self,):
        allProxys = []
        startPage = 0
        endPage = 1
        for index in range(startPage, endPage):
            content = self._requestUrl(index)
            list = self.parseProxyIpList(content)
            list = self.filterValidProxyIp(list)
            allProxys.append(list)
    def _async_raise(self,tid, exctype):
        import ctypes,inspect
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    def stop_thread(self,thread):
        self._async_raise(thread.ident, SystemExit)