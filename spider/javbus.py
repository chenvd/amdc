from meta.actor import Actor
from meta.meta import Meta
from spider.spider import Spider
import requests
from lxml import etree
from urllib.parse import urljoin

from spider.spider_exception import SpiderException


class JavbusSpider(Spider):
    host = "https://www.javbus.com/"
    name = 'Javbus'

    def get_info(self):

        url = urljoin(self.host, self.num)
        response = requests.get(url, allow_redirects=False)

        html = etree.HTML(response.text)

        meta = Meta()
        meta.num = self.num

        title_element = html.xpath("//h3")
        if title_element:
            title = title_element[0].text
            title_parts = title.split(" ")
            meta.title = " ".join(title_parts[1:])
        else:
            raise SpiderException('未找到匹配影片')

        premiered_element = html.xpath("//span[text()='發行日期:']")
        if premiered_element:
            meta.premiered = premiered_element[0].tail.strip()

        runtime_element = html.xpath("//span[text()='長度:']")
        if runtime_element:
            runtime = runtime_element[0].tail.strip()
            runtime = runtime.replace("分鐘", "")
            meta.runtime = runtime

        director_element = html.xpath("//span[text()='導演:']/../a")
        if director_element:
            director = director_element[0].text
            meta.director = director

        maker_element = html.xpath("//span[text()='製作商:']/../a")
        if maker_element:
            maker = maker_element[0].text
            meta.maker = maker

        publisher_element = html.xpath("//span[text()='發行商:']/../a")
        if publisher_element:
            publisher = publisher_element[0].text
            meta.publisher = publisher

        series_element = html.xpath("//span[text()='系列:']/../a")
        if series_element:
            series = series_element[0].text
            meta.series = series

        tag_elements = html.xpath("//span[@class='genre']//a[contains(@href,'genre')]")
        if tag_elements:
            tags = [tag.text for tag in tag_elements]
            meta.tags = tags

        actor_elements = html.xpath("//span[@class='genre']//a[contains(@href,'star')]")
        if actor_elements:
            actors = []
            for element in actor_elements:
                actor_url = element.get('href')
                actor_code = actor_url.split("/")[-1]
                actor_avatar = urljoin(self.host, f'/pics/actress/{actor_code}_a.jpg')
                actor = Actor(element.text, actor_avatar)
                actors.append(actor)
            meta.actors = actors

        cover_element = html.xpath("//a[@class='bigImage']")
        if cover_element:
            cover = cover_element[0].get("href")
            meta.cover = urljoin(self.host, cover)

        meta.website = url

        return meta
