# encoding: UTF-8
import scrapy
from urllib.parse import urljoin

from pwscrapy.items import PwCategoryScrapyItem

SITE_URL = "https://www.programmableweb.com"

class pwscrapy(scrapy.spiders.Spider):
    # scrapy crawl pwc -o categories.json
    # scrapy crawl pwc -s LOG_FILE=spider.log
    name = "pwc"
    # allowed_domains = ["programmableweb.com"] # 不必须，可选
    start_urls = [
        "https://www.programmableweb.com/category"
    ]

    def __init__(self):
        self.page_count = 1
        self.category_count = 0
        self.total_page_num = -1

    def parse(self, response):
        if self.total_page_num == -1:
            self.total_page_num = response.css('.pager-next a::text').extract()[0]
        self.logger.debug("----------"+str(self.page_count)+"/"+str(self.total_page_num)+"----------")

        for sel in response.css('.item-list .views-row'):
            category_pw_url = response.urljoin("".join(sel.css("a::attr(href)").extract())) # response.url会自动提取出当前页面url的主域名
            yield scrapy.Request(url=category_pw_url, callback=self.parse_category_details, dont_filter=True, priority=1)

        # 爬取下一页
        if self.page_count < int(self.total_page_num):
            next_page = "https://www.programmableweb.com/category?page=" + str(self.page_count)
            self.log("page_url: %s" % next_page)
            self.page_count += 1
            yield scrapy.Request(next_page, callback=self.parse, priority=0)
        
    def parse_category_details(self, response):
        self.category_count += 1
        item = PwCategoryScrapyItem()

        item['category_id'] = response.css('.region-header-right ul.menu a::attr(href)').extract()[1].split('/')[-1]
        item['category_name'] = response.css(".category-term-name::text").extract()[0]
        item['category_pw_url'] = response.url
        
        yield item