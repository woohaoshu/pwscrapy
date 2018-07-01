# encoding: UTF-8
import scrapy
from urllib.parse import urljoin

from pwscrapy.items import PwApiScrapyItem

SITE_URL = "https://www.programmableweb.com"

class pwscrapy(scrapy.spiders.Spider):
    # scrapy crawl pwa -o apis.json
    # scrapy crawl pwa -s LOG_FILE=spider.log
    name = "pwa"
    # allowed_domains = ["programmableweb.com"] # 不必须，可选
    start_urls = [
        "https://www.programmableweb.com/category/all/apis"
    ]

    def __init__(self):
        self.page_count = 0
        self.api_count = 0
        self.total_page_num = -1

    def parse(self, response):
        if self.total_page_num == -1:
            self.total_page_num = response.css('.pager-next a::text').extract()[0]
        self.logger.debug("----------"+str(self.page_count)+"/"+str(self.total_page_num)+"----------")

        for sel in response.xpath("//td[contains(@class,'col-md-3')]/a"):
            api_pw_url = response.urljoin("".join(sel.xpath("@href").extract())) # response.url会自动提取出当前页面url的主域名
            yield scrapy.Request(url=api_pw_url, callback=self.parse_api_details, dont_filter=True, priority=1)

        # 爬取下一页
        if self.page_count < int(self.total_page_num):
            next_page = "https://www.programmableweb.com/category/all/apis?page=" + str(self.page_count)
            self.log("page_url: %s" % next_page)
            self.page_count += 1
            yield scrapy.Request(next_page, callback=self.parse, priority=0)
        
    def parse_api_details(self, response):
        self.api_count += 1
        item = PwApiScrapyItem()

        item['api_id'] = response.css(".api-summary::attr(id)").extract()[0].split('-')[1]
        item['api_name'] = response.css(".breadcrumb .last::text").extract()[0]
        item['api_pw_url'] = response.url
        if len(response.css("#myTabContent .field:contains('API Portal')").extract()) != 0:
            item['api_url'] = response.css("#myTabContent .field:contains('API Portal') a::text").extract()[0]
        if len(response.css("#myTabContent .field:contains('Primary Category')").extract()) != 0:
            item['api_primary_category'] = response.css("#myTabContent .field:contains('Primary Category') a::text").extract()[0]
        if len(response.css("#myTabContent .field:contains('Secondary Categories')").extract()) != 0:
            item['api_secondary_category'] = response.css("#myTabContent .field:contains('Secondary Categories') a::text").extract()
        item['api_desc'] = response.css("#tabs-header-content > div > div.api_description.tabs-header_description").extract_first().strip("<div class=\"api_description tabs-header_description\">\n").strip(" </div>")

        yield item