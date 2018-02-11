# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShixisengspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    type = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    academic = scrapy.Field()
    work_date = scrapy.Field()
    work_time = scrapy.Field()
    work_opportunity = scrapy.Field()

    job_lure = scrapy.Field()
    job_description = scrapy.Field()

    company_description = scrapy.Field()

    job_update_time = scrapy.Field()
    job_deadline = scrapy.Field()

    detail_href = scrapy.Field()

