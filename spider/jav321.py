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
        no = self.get_html_no(url)
        if not no:
            no = self.get_html_no(urljoin(self.host, "/video/" + self.num))

        if not no:
            raise SpiderException('未找到匹配影片')

        meta = Meta()
        meta.num = self.num

        outline_element = no[0].xpath("./../../..//div[@class='row']")
        if len(outline_element) > 0:
            outline = outline_element[-1].xpath("./div")[0]
            if outline.text:
                meta.outline = outline.text.replace("\n", "")
                brs = outline.xpath('./br')
                if brs:
                    extra_outline = "".join(map(lambda i: i.tail, brs))
                    hr_index = extra_outline.find("----------------------")
                    if hr_index != -1:
                        meta.outline += (extra_outline[0:hr_index])
                    else:
                        meta.outline += extra_outline
        return meta

    def get_html_no(self, url):
        response = requests.get(url, allow_redirects=False)
        html = etree.HTML(response.text)

        no = html.xpath("//small")
        if no and no[0].text.strip() == self.num.lower():
            return no

    def generate_url(self):
        parts = self.num.split("-")
        url = "{0}{1:0>5d}".format(parts[0], int(parts[1]))
        return urljoin(self.host, "/video/" + url)
