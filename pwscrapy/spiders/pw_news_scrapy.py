# encoding: UTF-8
import scrapy
from urllib.parse import urljoin
import re

from pwscrapy.items import PwNewsScrapyItem

SITE_URL = "https://www.programmableweb.com"

class pwscrapy(scrapy.spiders.Spider):
    # scrapy crawl pwa -o news.json
    # scrapy crawl pwa -s LOG_FILE=spider.log
    name = "pwn"
    # allowed_domains = ["programmableweb.com"] # 不必须，可选
    start_urls = [
        "https://www.programmableweb.com/category/all/news"
    ]

    def __init__(self):
        self.page_count = 1
        self.news_count = 0

    def parse(self, response):
        total_page_num = response.css('.pager-next a::text').extract()
        self.logger.debug("----------"+str(self.page_count)+"/"+total_page_num[0]+"----------")

        # 爬取目录页信息
        for sel in response.css(".view-search-articles-solr>.view-content>.views-row"):
            item = PwNewsScrapyItem()
            news_pw_url = response.urljoin("".join(sel.css("h2>a::attr(href)").extract())) # response.url会自动提取出当前页面url的主域名
            item["news_page_count"] = self.page_count
            item["news_pw_url"] = news_pw_url
            item["news_name"] = sel.css("h2>a::text").extract()[0]
            if len(response.css(".pull-left-wrapper .content-type>a::text").extract()) != 0:
                item["news_article_type"] = sel.css(".pull-left-wrapper .content-type>a::text").extract()[0]
            if len(response.css(".pull-left-wrapper .name>a::text").extract()) != 0:
                item["news_author"] = sel.css(".pull-left-wrapper .name>a::text").extract()[0]
            if len(response.css(".text>span::text").extract()) != 0:
                item["news_abstract"] = sel.css(".text>span::text").extract()[0]
            yield scrapy.Request(url=news_pw_url, meta={'item':item}, callback=self.parse_news_details, dont_filter=True)

        # 爬取下一页
        if self.page_count < int(total_page_num[0]):
            next_page = "https://www.programmableweb.com/category/all/news?page=" + str(self.page_count)
            self.log("page_url: %s" % next_page)
            self.page_count += 1
            yield scrapy.Request(next_page, callback=self.parse)
        
    def parse_news_details(self, response):
        item = response.meta['item']
        self.news_count += 1
        item['news_count'] = self.news_count
        item['news_date'] = response.url.split("/")[-3:]
        if len(response.css("span[data-str-brand] a::text").extract()) != 0:
            item['news_category'] = response.css("span[data-str-brand] a::text").extract()
        if len(response.css("span[data-str-content] .field-item p").extract()) != 0:
            news_content = " ".join(response.css("span[data-str-content] .field-item p").extract())
            news_content = re.compile(r'<[^>]+>', re.S).sub('', news_content) # [^>]+ 不是^的任意字符
            item['news_content'] = news_content
        yield item