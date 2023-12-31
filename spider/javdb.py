import re
from urllib.parse import urljoin
from lxml import etree

from meta.actor import Actor
from meta.meta import Meta
from spider.spider import Spider
import requests

from spider.spider_exception import SpiderException


class JavdbSpider(Spider):
    host = "https://javdb.com"
    name = 'Javdb'
    avatar_host = 'https://c0.jdbstatic.com/avatars/'

    def get_info(self):

        url = self.search()
        if not url:
            raise SpiderException('未找到匹配影片')

        meta = Meta()
        meta.num = self.num

        response = requests.get(url)
        html = etree.HTML(response.content, parser=etree.HTMLParser(encoding='utf-8'))

        title_element = html.xpath("//strong[@class='current-title']")
        if title_element:
            title = title_element[0].text.strip()
            title_parts = title.split(" ")
            meta.title = " ".join(title_parts[1:])

        premiered_element = html.xpath("//strong[text()='日期:']/../span")
        if premiered_element:
            meta.premiered = premiered_element[0].text

        runtime_element = html.xpath("//strong[text()='時長:']/../span")
        if runtime_element:
            runtime = runtime_element[0].text
            runtime = runtime.replace(" 分鍾", "")
            meta.runtime = runtime

        director_element = html.xpath("//strong[text()='導演:']/../span/a")
        if director_element:
            director = director_element[0].text
            meta.director = director

        maker_element = html.xpath("//strong[text()='片商:']/../span/a")
        if maker_element:
            maker = maker_element[0].text
            meta.maker = maker

        publisher_element = html.xpath("//strong[text()='發行:']/../span/a")
        if publisher_element:
            publisher = publisher_element[0].text
            meta.publisher = publisher

        series_element = html.xpath("//strong[text()='系列:']/../span/a")
        if series_element:
            series = series_element[0].text
            meta.series = series

        tag_elements = html.xpath("//a[contains(@href,'/tags?')]")
        if tag_elements:
            tags = [tag.text for tag in tag_elements]
            meta.tags = tags

        actor_elements = html.xpath("//strong[@class='symbol female']")
        if actor_elements:
            actors = []
            for element in actor_elements:
                actor_element = element.xpath('./preceding-sibling::a[1]')[0]
                actor_url = actor_element.get('href')
                actor_code = actor_url.split("/")[-1]
                actor_avatar = urljoin(self.avatar_host, f'{actor_code[0:2]}/${actor_code}.jpg')
                actor = Actor(actor_element.text, actor_avatar)
                actors.append(actor)
            meta.actors = actors

        cover_element = html.xpath("//img[@class='video-cover']")
        if cover_element:
            meta.cover = cover_element[0].get("href")

        score_elements = html.xpath("//span[@class='score-stars']/../text()")
        if score_elements:
            score_text = str(score_elements[0])
            pattern_result = re.search(r"(\d+\.\d+)分", score_text)
            score = pattern_result.group(1)
            meta.rating = score

        meta.website = url

        return meta

    def search(self):
        url = urljoin(self.host, f"/search?q={self.num}&f=all")
        response = requests.get(url)

        html = etree.HTML(response.content)
        matched_element = html.xpath(fr"//strong[text()='{self.num}']/../..")
        if matched_element:
            code = matched_element[0].get('href')
            return urljoin(self.host, code)
