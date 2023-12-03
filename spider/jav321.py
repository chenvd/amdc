from urllib.parse import urljoin

import requests
from lxml import etree

from meta.meta import Meta
from spider.spider import Spider
from spider.spider_exception import SpiderException


class Jav321Spider(Spider):
    host = "https://www.jav321.com/"
    name = 'Jav321'

    def get_info(self):
        url = self.generate_url()
        response = requests.get(url, allow_redirects=False)
        html = etree.HTML(response.text)

        no = html.xpath("//small")
        if not no or no[0].text.strip() != self.num.lower():
            raise SpiderException('未找到匹配影片')

        meta = Meta()
        meta.num = self.num

        outline_element = no[0].xpath("./../../..//div[@class='row']")
        if len(outline_element) > 0:
            outline = outline_element[-1].xpath("./div")[0]
            meta.outline = outline.text

        return meta

    def generate_url(self):
        parts = self.num.split("-")
        url = "{0}{1:0>5d}".format(parts[0], int(parts[1]))
        return urljoin(self.host, "/video/" + url)
