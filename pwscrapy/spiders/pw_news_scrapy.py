# encoding: UTF-8
import scrapy
from urllib.parse import urljoin

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
        self.page_count = 0
        self.news_count = 0

    def parse(self, response):
        total_page_num = response.css('.pager-next a::text').extract()
        self.logger.debug("----------"+str(self.page_count+1)+"/"+total_page_num[0]+"----------")

        for sel in response.xpath("//td[contains(@class,'col-md-3')]/a"):
            news_pw_url = response.urljoin("".join(sel.xpath("@href").extract())) # response.url会自动提取出当前页面url的主域名
            yield scrapy.Request(url=news_pw_url, callback=self.parse_news_details, dont_filter=True)

        # 爬取下一页
        if self.page_count < int(total_page_num[0]):
            next_page = "https://www.programmableweb.com/category/all/news?page=" + str(self.page_count)
            self.log("page_url: %s" % next_page)
            self.page_count += 1
            yield scrapy.Request(next_page, callback=self.parse)
        
        

    def parse_news_details(self, response):
        self.news_count += 1
        item = PwNewsScrapyItem()

        item['news_name'] = response.css(".news-summary::attr(id)").extract()[0].split('-')[1]
        item['news_pw_url'] = response.url
        item['news_date'] = response.url
        item['news_author'] = response.url
        item['news_article_type'] = response.url
        if len(response.css("").extract()) != 0:
            item['news_category'] = response.css("").extract()[0]
        item['news_desc'] = response.css("").extract_first().strip("").strip(" </div>")

        yield item