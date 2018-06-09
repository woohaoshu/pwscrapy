# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PwApiScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    api_id = scrapy.Field()
    api_name = scrapy.Field()
    api_pw_url = scrapy.Field()
    api_url = scrapy.Field()
    api_primary_category = scrapy.Field()
    api_secondary_category = scrapy.Field()
    api_desc = scrapy.Field()

class PwMashupScrapyItem(scrapy.Item):
    mashup_id = scrapy.Field()
    mashup_name = scrapy.Field()
    mashup_pw_url = scrapy.Field()
    mashup_url = scrapy.Field()
    mashup_category = scrapy.Field()
    mashup_related_apis = scrapy.Field()
    mashup_desc = scrapy.Field()

class PwNewsScrapyItem(scrapy.Item):
    news_name = scrapy.Field()
    news_pw_url = scrapy.Field()
    news_date = scrapy.Field()
    news_author = scrapy.Field()
    news_article_type = scrapy.Field()
    news_category = scrapy.Field()
    news_content = scrapy.Field()