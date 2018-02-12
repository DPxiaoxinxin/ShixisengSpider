#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: xxx
# Platform: platform independent, currently running on linux like system
# Language: Python2.6 or 2.7
#
# Update history:
#
# Name                Version                Date                Detail
# xxx                 0.0.1                  xxth xx xxxx       Initialization
#
# TO DO:
# 



shixiseng_cache = {
    "\uf739": "0",
    "\uf546": "0",
    "\uf7a3": "1",
    "\uf566": "1",
    "\ue1d1": "2",
    "\ue7be": "2",
    "\ue340": "3",
    "\uec03": "3",
    "\uf7e4": "4",
    "\uf167": "5",
    "\uf226": "5",
    "\uecf1": "6",
    "\uf55d": "7",
    "\ue256": "8",
    "\ue5aa": "8",
    "\ue50a": "9",
    "\uef79": "软",
    "\uf334": "件",
    "\uef09": "生"
    # "0": ["\uf739", "\uf546"],
    # "1": ["\uf7a3", "\uf566"],
    # "2": ["\ue1d1", "\ue7be"],
    # "3": ["\ue340", "\uec03"],
    # "4": ["\uf7e4", "\uf7e4"],
    # "5": ["\uf167", "\uf226"],
    # "6": ["\uecf1", "\uecf1"],
    # "7": ["\uf55d", ],
    # "8": ["\ue256", "\ue5aa"],
    # "9": ["\ue50a", "\ue50a"],
}
def replcae_cache(data):
    for key in data.keys():
        for oldStr in shixiseng_cache.keys():
            if oldStr in data[key]:
                data[key] = data[key].replace(oldStr, shixiseng_cache[oldStr])
    return data

if __name__ == "__main__":
    data = {'academic': '本科',
         'company': '友缘在线',
         'company_description': '',
         'detail_href': 'https://www.shixiseng.com/intern/inn_wdlwx7rma21c',
         'job_deadline': '\ue7be\uf546\uf566\ue5aa-\uf546\ue7be-\uf566\ue50a',
         'job_description': '',
         'job_lure': '职位诱惑：专业指导 更快速成长',
         'job_update_time': '\ue7be\uf546\uf566\ue5aa-\uf546\ue7be-\uf566\ue7be '
                            '\uf566\uf566:\uf566\uf546:\uec03\uf566',
         'location': '北京',
         'name': '产品实习\uef09',
         'salary': '\uf566\uec03\uf226-\uf566\uecf1\uf226／天',
         'type': ' - 产品',
         'work_date': '\uf7e4天／周',
         'work_opportunity': '',
         'work_time': '实习\uec03个月'}

    data = replcae_cache(data)

    print(data)
