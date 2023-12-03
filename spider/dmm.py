from urllib.parse import urljoin

import requests
from lxml import etree

from meta.meta import Meta
from spider.spider import Spider
from spider.spider_exception import SpiderException


class DmmSpider(Spider):
    host = "https://www.dmm.co.jp"
    name = 'DMM'

    def get_info(self):
        url = self.get_real_page()
        response = requests.get(url)
        if response.status_code == 404:
            raise SpiderException('未找到匹配影片')

        meta = Meta()
        meta.num = self.num

        html = etree.HTML(response.text)
        outline_element = html.xpath("//div[@class='clear']/following-sibling::div[1]")
        if outline_element:
            outline = outline_element[0]
            meta.outline = outline.text.replace("\n", "")
            brs = outline.xpath('./br')
            if brs:
                meta.outline += "".join(map(lambda i: i.tail, brs))

        return meta

    def generate_url(self):
        parts = self.num.split("-")
        url = "{0}{1:0>5d}".format(parts[0], int(parts[1]))
        return urljoin(self.host, f"/digital/videoa/-/detail/=/cid={url}/")

    def get_real_page(self):
        url = self.generate_url()
        response = requests.get(url)
        html = etree.HTML(response.text)
        check_element = html.xpath("//div[@class='ageCheck__btn']/a")
        if not check_element:
            raise Exception("找不到年龄确认按钮")
        return check_element[1].get('href')
