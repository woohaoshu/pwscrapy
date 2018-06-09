import scrapy
import time

class Spider(scrapy.Spider):
    name = 'ip'
    allowed_domains = []

    def start_requests(self):

        url = 'http://ip.chinaz.com/getip.aspx'
        # url = 'http://httpbin.org/get'

        for i in range(4):
            print("++++++++++++++++++++++++++++++++++++++++++++",i)
            time.sleep(0.1)
            yield scrapy.Request(url=url, meta={"download_timeout":2}, callback=self.parse, dont_filter=True)

    def parse(self,response):
        print("-------------------------------------------")
        print(response.text)