# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import codecs
from bs4 import BeautifulSoup
import urllib.request
import http.client
import time
import _thread
import threading
import codecs


class PwscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PwscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 随机User-Agent
class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent

# 随机Proxy
class ProxyMiddleware(object):
    '''
    设置Proxy
    '''

    def __init__(self):
        self.ip = []
        self.inFile = codecs.open('ProxyIP/proxy.txt', 'r+', encoding='utf8')
        self.https_outFile = codecs.open('ProxyIP/https_verified.txt', 'r+', encoding='utf8')
        self.lock = threading.Lock()
        print(u"国内透明：" + str(self.getProxyList()))
        self.inFile.close()
        self.inFile = codecs.open('ProxyIP/proxy.txt', 'r+', encoding='utf8')
        print(u"\n验证代理的有效性：")
        all_thread = []
        for i in range(10):
            t = threading.Thread(target=self.verifyProxyList)
            all_thread.append(t)
            t.start()
        for t in all_thread:
            t.join()
        self.https_outFile.close()
        self.https_outFile = codecs.open('ProxyIP/https_verified.txt', 'r+', encoding='utf8')        
        for line in self.https_outFile.readlines():
            self.ip.append(line.strip('\n'))
        self.inFile.close()
        self.https_outFile.close()
        print("爬取到的ip列表："+",".join(self.ip))
        # 3.开启一个线程，动态更新ip pool
        _thread.start_new_thread(self.proxyThread, (180, ))
        print("自动更新代理线程已开启")

    # def __init__(self, ip):
    #     self.ip = ip

    # @classmethod
    # def from_crawler(cls, crawler):
        # 1.从配置文件中读ip pool
        # return cls(ip=crawler.settings.get('PROXIES'))

        # 2.从文件中读ip pool
        # proxies = []
        # with codecs.open('ProxyIP/https_verified.txt' , 'r', encoding='utf8') as f:
        #     for line in f.readlines():
        #         proxies.append(line.strip('\n'))
        # print(proxies)
        # return cls(ip = proxies)


    def process_request(self, request, spider):
        ip = random.choice(self.ip)
        spider.logger.info("++++++++++++----------------Current IP: "+ip+"++++++++++++++++++++++++++++")
        request.meta['proxy'] = ip

    def process_response(self, request, response, spider):
        if response.status != 200:
            spider.logger.info("||||||||||||||||||||||")
            ip = random.choice(self.ip)
            spider.logger.info("++++++++++++++++++++++++++++Current IP: "+ip+"++++++++++++++++++++++++++++")
            request.meta['proxy'] = ip
            return request
        return response

    def proxyThread(self, delay):
        while True:
            self.inFile = codecs.open('ProxyIP/proxy.txt', 'r+', encoding='utf8')
            self.https_outFile = codecs.open('ProxyIP/https_verified.txt', 'r+', encoding='utf8')
            self.lock = threading.Lock()
            print(u"国内透明：" + str(self.getProxyList()))
            self.inFile.close()
            self.inFile = codecs.open('ProxyIP/proxy.txt', 'r+', encoding='utf8')
            print(u"\n验证代理的有效性：")
            all_thread = []
            for i in range(10):
                t = threading.Thread(target=self.verifyProxyList)
                all_thread.append(t)
                t.start()
            for t in all_thread:
                t.join()
            self.https_outFile.close()
            self.https_outFile = codecs.open('ProxyIP/https_verified.txt', 'r+', encoding='utf8')
            for line in self.https_outFile.readlines():
                self.ip.append(line.strip('\n'))
            self.inFile.close()
            self.https_outFile.close()
            print("爬取到的ip列表："+",".join(self.ip))
            time.sleep(delay)

    def getProxyList(self, targeturl="http://www.xicidaili.com/nt/"):
        countNum = 0
        requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
        for page in range(1, 2):
            url = targeturl + str(page)
            request = urllib.request.Request(url, headers=requestHeader)
            html_doc = urllib.request.urlopen(request).read()
        
            soup = BeautifulSoup(html_doc, "html.parser")
            trs = soup.find('table', id='ip_list').find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                if tds[0].find('img') is None :
                    nation = '未知'
                    locate = '未知'
                else:
                    nation =   tds[0].find('img')['alt'].strip()
                    locate  =   tds[3].text.strip()
                ip      =   tds[1].text.strip()
                port    =   tds[2].text.strip()
                anony   =   tds[4].text.strip()
                protocol=   tds[5].text.strip()
                speed   =   tds[6].find('div')['title'].strip()
                time    =   tds[8].text.strip()
                
                self.inFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol,speed, time))
                countNum += 1
        return countNum

    def verifyProxyList(self):
        requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
        myurl = 'https://www.programmableweb.com'
        while True:
            self.lock.acquire()
            ll = self.inFile.readline().strip()
            self.lock.release()
            if len(ll) == 0: break
            line = ll.strip().split('|')
            protocol= line[5]
            ip      = line[1]
            port    = line[2]
            # print(ip + ":" + port + "\n")
            if(protocol == "HTTPS"):
                try:
                    conn = http.client.HTTPConnection(ip, port, timeout=5.0)
                    conn.request(method = 'GET', url = myurl, headers = requestHeader )
                    res = conn.getresponse()
                    self.lock.acquire()
                    print("+++Success:" + ip + ":" + port)
                    self.https_outFile.write(ip + ":" + port + "\n")
                    self.lock.release()
                except:
                    print("---Failure:" + ip + ":" + port)
        
