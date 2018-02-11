# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from datetime import date


class ShixisengspiderPipeline(object):
    def __init__(self):
        self.file_obj = open("shixiseng{date}.csv".format(date=date.today()), "w", encoding='utf_8_sig', newline="")
        self._fields = ["name", "company", "type", "location", "salary", "academic", "work_date", "work_time",
                        "work_opportunity", "job_lure", "job_description", "company_description", "job_update_time",
                        "job_deadline", "detail_href"]
        self._dictwriter = csv.DictWriter(self.file_obj, fieldnames=self._fields)
        self._dictwriter.writerow({"name": "职位名称", "company": "公司", "type": "类别", "location": "工作地点",
                                   "salary": "待遇",
                                   "academic": "学历", "work_date": "每周工作时间", "work_time": "工作时间",
                        "work_opportunity": "是否提供转正", "job_lure": "职位诱惑", "job_description": "职位描述",
                                   "company_description": "公司描述",
                                   "job_update_time": "岗位刷新时间",
                        "job_deadline": "截止时间", "detail_href": "具体日期"})

    def process_item(self, item, spider):
        self._dictwriter.writerow(item._values)
        return item

    def close_spider(self, spider):
        self.file_obj.close()
