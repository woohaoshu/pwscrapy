# encoding: UTF-8
import scrapy
from urllib.parse import urljoin

from pwscrapy.items import PwMashupScrapyItem

SITE_URL = "https://www.programmableweb.com"

class pwscrapy(scrapy.spiders.Spider):
    name = "pwm"    # cmd: scrapy crawl pwm -o mashups.json
    # allowed_domains = ["programmableweb.com"] # 不必须，可选
    start_urls = [
        "https://www.programmableweb.com/category/all/mashups"
    ]

    def __init__(self):
        self.page_count = 0
        self.mashup_count = 0

    def parse(self, response):
        total_page_num = response.css('.pager-next a::text').extract()
        self.logger.debug("----------"+(self.page_count+1)+"/"+total_page_num[0]+"----------")

        for sel in response.xpath("//td[contains(@class,'col-md-3')]/a"):
            mashup_pw_url = response.urljoin("".join(sel.xpath("@href").extract())) # response.url会自动提取出当前页面url的主域名
            yield scrapy.Request(url=mashup_pw_url, callback=self.parse_mashup_details)

        # 爬取下一页
        if self.page_count < int(total_page_num[0]):
            next_page = "https://www.programmableweb.com/category/all/mashups?page=" + str(self.page_count)
            self.log("page_url: %s" % next_page)
            self.page_count += 1
            yield scrapy.Request(next_page, callback=self.parse)
        
        

    def parse_mashup_details(self, response):
        self.mashup_count += 1
        item = PwMashupScrapyItem()
        item['mashup_id'] = response.css(".node-summary::attr(id)").extract()[0].split('-')[1]
        item['mashup_name'] = response.css(".breadcrumb .last::text").extract()[0]
        item['mashup_pw_url'] = response.url
        if len(response.css("#myTabContent .field:contains('URL')").extract()) != 0:
            item['mashup_url'] = response.css("#myTabContent .field:contains('URL') a::text").extract()[0]
        if len(response.css("#myTabContent .field:contains('Categories')").extract()) != 0:
            item['mashup_category'] = response.css("#myTabContent .field:contains('Categories') a::text").extract()
        if len(response.css("#myTabContent .field:contains('Related APIs')").extract()) != 0:
            item['mashup_related_apis'] = response.css("#myTabContent .field:contains('Related APIs') a::text").extract()
        item['mashup_desc'] = response.css(".field-type-text-with-summary .field-item").extract_first().strip("<div class=\"field-item even\">").strip(" </div>")
        yield item