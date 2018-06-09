# encoding=utf8

from bs4 import BeautifulSoup
import urllib.request
import http.client
import threading
import importlib,sys
import codecs
importlib.reload(sys)

inFile = codecs.open('proxy.txt', encoding='utf8')
https_outFile = codecs.open('https_verified.txt', 'w', encoding='utf8')
http_outFile = codecs.open('http_verified.txt', 'w', encoding='utf8')
lock = threading.Lock()

def getProxyList(targeturl="http://www.xicidaili.com/nn/"):
    countNum = 0
    proxyFile = codecs.open('proxy.txt' , 'a', encoding='utf8')
    
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    
    
    for page in range(1, 3):
        url = targeturl + str(page)
        #print url
        request = urllib.request.Request(url, headers=requestHeader)
        html_doc = urllib.request.urlopen(request).read()
    
        soup = BeautifulSoup(html_doc, "html.parser")
        # print soup
        trs = soup.find('table', id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            #国家
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
            
            proxyFile.write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol,speed, time) )
            # proxyFile.write('\"%s:%s\"\n' % (ip, port) )
            #print '%s=%s:%s' % (protocol, ip, port)
            countNum += 1
    
    proxyFile.close()
    return countNum
    
def verifyProxyList():
    '''
    验证代理的有效性
    '''
    requestHeader = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}
    myurl = 'https://www.programmableweb.com'
    # myurl = 'http://ip.chinaz.com/getip.aspx'
    # myurl = 'http://httpbin.org/get'

    while True:
        lock.acquire()
        ll = inFile.readline().strip()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        protocol= line[5]
        ip      = line[1]
        port    = line[2]
        
        if(protocol == "HTTPS"):
            try:
                conn = http.client.HTTPConnection(ip, port, timeout=5.0)
                conn.request(method = 'GET', url = myurl, headers = requestHeader )
                res = conn.getresponse()
                lock.acquire()
                print("+++Success:" + ip + ":" + port)
                # outFile.write(ll + "\n")
                https_outFile.write(ip + ":" + port + "\n")
                lock.release()
            except:
                print("---Failure:" + ip + ":" + port)
        else:
            try:
                conn = http.client.HTTPConnection(ip, port, timeout=5.0)
                conn.request(method = 'GET', url = myurl, headers = requestHeader )
                res = conn.getresponse()
                lock.acquire()
                print("+++Success:" + ip + ":" + port)
                # outFile.write(ll + "\n")
                http_outFile.write(ip + ":" + port + "\n")
                lock.release()
            except:
                print("---Failure:" + ip + ":" + port)
        
    
if __name__ == '__main__':
    tmp = codecs.open('proxy.txt' , 'w', encoding='utf8')
    tmp.write("")
    tmp.close()
    # proxynum = getProxyList("http://www.xicidaili.com/nn/")
    # print(u"国内高匿：" + str(proxynum))
    proxynum = getProxyList("http://www.xicidaili.com/nt/")
    print(u"国内透明：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wn/")
    # print(u"国外高匿：" + str(proxynum))
    # proxynum = getProxyList("http://www.xicidaili.com/wt/")
    # print(u"国外透明：" + str(proxynum))

    print(u"\n验证代理的有效性：")
    
    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()
        
    for t in all_thread:
        t.join()
    
    inFile.close()
    https_outFile.close()
    http_outFile.close()
    print("All Done.")

