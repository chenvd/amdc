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
        response = requests.post(urljoin(self.host, '/search'), data={'sn': self.num})
        html = etree.HTML(response.text)

        no = html.xpath("//small")
        if not no or no[0].text.strip() != self.num.lower():
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
