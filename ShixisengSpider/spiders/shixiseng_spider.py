# -*- coding: utf-8 -*-
import urllib

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ShixisengSpider.items import ShixisengspiderItem as Item

from utils.util import replcae_cache


class ShixisengSpider(CrawlSpider):
    name = 'shixiseng'
    allowed_domains = ['www.shixiseng.com']
    start_urls = ['https://www.shixiseng.com/interns?p=1']

    rules = (
        Rule(LinkExtractor(allow='/interns\?p=\d+$',
                           deny='/user/register\?next=/interns\?p=\d+$'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        nodes = response.xpath("//div[@class='list']")
        for node in nodes:
            item = Item()
            item["name"] = node.xpath(".//div[@class='names cutom_font']/a/text()").extract()[0]
            item["company"] = node.xpath(".//div[@class='part']/a/text()").extract()[0]
            item["type"] = node.xpath(".//div[@class='part']/text()").extract()[0]
            item["location"] = node.xpath(".//div[@class='addr']/span/text()").extract()[0]
            item["detail_href"] = "https://www.shixiseng.com" + node.xpath(".//div[@class='names cutom_font']/a/@href").extract()[0]
            yield scrapy.Request(item["detail_href"], meta={"item": item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta["item"]
        item["salary"] = response.xpath("//span[@class='job_money cutom_font']/text()").extract()[0]
        item["academic"] = response.xpath("//span[@class='job_academic']/text()").extract()[0]
        item["work_date"] = response.xpath("//div[@class='job_msg']/span[4]/text()").extract()[0]
        item["work_time"] = response.xpath("//div[@class='job_msg']/span[5]/text()").extract()[0]
        try:
            item["work_opportunity"] = response.xpath("//div[@class='job_msg']/span[6]/text()").extract()[0]
        except Exception as e:
            item["work_opportunity"] = ""
        item["job_lure"] = response.xpath("//div[@class='job_good']/text()").extract()[0]
        item["job_description"] = "\n".join(response.xpath("//div[@class='con-job job_introduce']//div[@class='job_detail']/span/text()").extract())
        if item["job_description"] == "":
            item["job_description"] = "\n".join(
                response.xpath("//div[@class='con-job job_introduce']/descendant::text()").extract())
        item["company_description"] = ""
        for node in response.xpath("//div[@class='con-job con-com_introduce/div']"):
            item["company_description"] += node.xpath("./div/text()").extract()[0]
        if item["company_description"] == "":
            item["company_description"] = "\n".join(response.xpath("//div[@class='con-job con-com_introduce']/descendant::text()").extract())
        item["job_update_time"] = response.xpath("//div[@class='job_date ']/span/text()").extract()[0]
        item["job_deadline"] = response.xpath("//div[@class='con-job deadline']/div[2]/text()").extract()[0]
        item = replcae_cache(item)
        yield item
