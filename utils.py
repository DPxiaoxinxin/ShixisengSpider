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
import base64
import struct
import zlib
from tempfile import NamedTemporaryFile

from fontTools.ttLib import TTFont

def woff_headers(infile):
    WOFFHeader = {'signature': struct.unpack(">I", infile.read(4))[0],
                  'flavor': struct.unpack(">I", infile.read(4))[0],
                  'length': struct.unpack(">I", infile.read(4))[0],
                  'numTables': struct.unpack(">H", infile.read(2))[0],
                  'reserved': struct.unpack(">H", infile.read(2))[0],
                  'totalSfntSize': struct.unpack(">I", infile.read(4))[0],
                  'majorVersion': struct.unpack(">H", infile.read(2))[0],
                  'minorVersion': struct.unpack(">H", infile.read(2))[0],
                  'metaOffset': struct.unpack(">I", infile.read(4))[0],
                  'metaLength': struct.unpack(">I", infile.read(4))[0],
                  'metaOrigLength': struct.unpack(">I", infile.read(4))[0],
                  'privOffset': struct.unpack(">I", infile.read(4))[0],
                  'privLength': struct.unpack(">I", infile.read(4))[0]}
    return WOFFHeader


def get_dict_numb_from_woff(path):
    char_num = []
    dict_num = dict()
    with open(path, "rb") as f:
        _woff_headers = woff_headers(f)
        TableDirectoryEntries = []

        for i in range(0, _woff_headers['numTables']):
            TableDirectoryEntries.append({'tag': struct.unpack(">I", f.read(4))[0],
                                          'offset': struct.unpack(">I", f.read(4))[0],
                                          'compLength': struct.unpack(">I", f.read(4))[
                                              0],
                                          'origLength': struct.unpack(">I", f.read(4))[
                                              0],
                                          'origChecksum': struct.unpack(">I", f.read(4))[
                                              0]})
        for TableDirectoryEntry in TableDirectoryEntries:
            f.seek(TableDirectoryEntry['offset'])
            compressedData = f.read(TableDirectoryEntry['compLength'])
            if TableDirectoryEntry['compLength'] != TableDirectoryEntry['origLength']:
                uncompressedData = zlib.decompress(compressedData)
            else:
                uncompressedData = compressedData
            if "uni" in uncompressedData:
                for cha in uncompressedData.split("\x07"):
                    if "uni" in cha:
                        char_num.append(cha.strip("\x00"))
        for k, _unicode in enumerate(char_num):
            dict_num[_unicode] = str(k)
        dict_num['.'] = '.'
        return dict_num

def parse_font_face(font_face):
    """解析unicode值和十进制数字的映射。
    猫眼使用font_face进行反爬虫，html中的数字都是类似'&#xe4f9'这样的字符，这些字符和数字的映射被定义在字体文件中，
    经过渲染会显示为正常的数字。
    有两种方式应对这种反爬虫方式：1.解析字体文件，分析出映射关系；2.对网页截图，进行OCR。 这里使用第一种方法。
    字体文件被定义在页面上，是一串base64编码的字符串。对其解码后使用fontTools工具解析，获取glyph order，即是映射关系。
    :param font_face: 编码后的字体文件字符串
    :return: dict of unicode and number string
    """
    font_data = base64.b64decode(font_face)
    with NamedTemporaryFile('w+b', dir="./", delete=False) as fp:
        fp.write(font_data)
        fp.seek(0)

        font = TTFont(fp.name)
        # font.saveXML("./font.xml")
        # font = get_dict_numb_from_woff(fp.name)
        # return font

        # getGlyphOrder()返回这样的列表：['glyph00000', 'x', 'uniEFD3', 'uniEC6A', 'uniE4F9', 'uniF8F3', 'uniF324',
        #  'uniE7F7', 'uniE711', 'uniF1C9', 'uniE21D', 'uniF1D7']
        #
        # 除去前两个元素，索引和元素值既是我们需要的映射关系，第三个元素对应0，第四个元素对应1...
        # 将其转换为{'\uefd3': '0', '\uec6a': '1', '\ue4f9': '2', '\uf8f3': '3', '\uf324': '4', '\ue7f7': '5',
        #  '\ue711': '6','\uf1c9': '7', '\ue21d': '8', '\uf1d7': '9'}这样的字典return出去

        # {'job_deadline': '\ue1d1\uf739\uf7a3\ue256-\uf739\ue1d1-\ue1d1\uf167',
        #  'job_description': '岗位描述\n 1、 微信平台文案的撰写、每周进行图文推送；\n 2、 微信社群的维护推广；\n 3、互联网媒体平台的内容发布及维护（大众点评、百度百科等）；\n 4、报表统计；\n5、后台运营数据的收集、分析；\n6、协助门店进行线下活动的推广和宣传。\n 任职要求：\n 1、 专科及以上学历，应届生亦可，有微信平台运营推广经验尤佳\n 2、 具备一定的文案写作功底及活动策划能力\n 3、 社交达人，熟悉各类社交软件，尤其是微信\n 4、 有责任心，具备良好的沟通能力、表达能力、分析能力',
        #  'salary': '\uf7a3\ue1d1\uf739-\uf7a3\ue256\uf739／天',
        #  'detail_href': 'https://www.shixiseng.com/intern/inn_f2hqh2jwdepu', 'work_time': '实习\ue67c个月',
        #  'company_description': '', 'job_lure': '职位诱惑：发展空间大，快速成长，公平薪资待遇',
        #  'job_update_time': '\ue1d1\uf739\uf7a3\ue256-\uf739\ue1d1-\uf7a3\uf7a3 \uf7a3\ueaca:\uf167\ue67c:\uf739\ue6ec',
        #  'name': '微信运营推\ue6a9', 'work_date': '\uea7f天／周', 'work_opportunity': '提供转正机会', 'company': '润\uf5d8通讯',
        #  'type': ' - 新媒体', 'location': '上海', 'academic': '大专'}

        # {'job_deadline': '\ue1d1\uf739\uf7a3\ue256-\uf739\ue1d1-\ue1d1\uf167',
        #  'job_description': '【岗位内容】\n 1、微信及推广文案的选题、编排及撰写\n 2、短视频的拍摄剪辑\n 3、基础的图片处理设计\n 4、线上活动方案的策划\n 5、 \xa0微信公众平台的日常运营，善于挖掘和分析网友使用习惯、情感及体验感受，充分利用各类社会化媒体工具来实现网站推广、口碑积累与粉丝沉淀',
        #  'salary': '\uf7a3\ue1d1\uf739-\uf7a3\ue256\uf739／天',
        #  'detail_href': 'https://www.shixiseng.com/intern/inn_5tehdnti2lck', 'work_time': '实习\ue340个月',
        #  'company_description': '', 'job_lure': '职位诱惑：绩效奖金/交通补助/餐补',
        #  'job_update_time': '\ue1d1\uf739\uf7a3\ue256-\uf739\ue1d1-\uf7a3\uf7a3 \uf7a3\ueaca:\uf167\ue67c:\uea7f\ue340',
        #  'name': '新媒体推\ue6a9运营', 'work_date': '\uf167天／周', 'work_opportunity': '', 'company': '润\uf5d8通讯',
        #  'type': ' - 新媒体', 'location': '上海', 'academic': '不限'}
        print(font)
        for i in font.getGlyphOrder():
            print(i.encode("utf-8"))
        # return {eval("u\"" + '\\u' + value.split('uni')[-1].lower() + "\""): str(key) for key, value
        #         in dict(enumerate(font.getGlyphOrder()[2:])).items()}


if __name__ == "__main__":
    woff = "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"
    output = parse_font_face(woff)
    print(output)