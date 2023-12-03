import os
import shutil

import image
from spider.dmm import DmmSpider
from spider.jav321 import Jav321Spider
from spider.javbus import JavbusSpider
from spider.javdb import JavdbSpider
from spider.spider import Spider

from utils import number_parse, nfo_generator
from utils.logger import logger

input_path = os.getenv("INPUT_PATH")
output_path = os.getenv("OUTPUT_PATH")
size_limit = int(os.getenv("SIZE_LIMIT"))


def run():
    for root, dirs, files in os.walk(input_path):
        for file in files:
            path = os.path.join(root, file)
            size = os.stat(path).st_size
            if size < (size_limit * 1024 * 1024):
                continue
            try:
                logger.info("=================================================================")
                scrapy(path, file)
                logger.info("=================================================================")
            except Exception as e:
                logger.error(f'影片《{file}》获取信息失败', exc_info=True)


def scrapy(path, file_name):
    logger.info(f"找到影片《{path}》")
    number = number_parse.parse(file_name)
    if not number:
        logger.info(f"识别影片信息失败{path}，请检查文件名!!!")
        return
    else:
        logger.info(f"识别影片信息成功：{number.num}, "
                    f"中文字幕：{number.is_ch}，"
                    f"流出：{number.is_leak}，"
                    f"无码：{number.is_uncensored}")

    spiders = (
        JavbusSpider(number.num),
        JavdbSpider(number.num),
        DmmSpider(number.num),
        Jav321Spider(number.num),
    )
    meta = Spider.combine(*spiders)
    if not meta:
        logger.info("无法获取影片信息，请确认文件名或稍后再试!!!")
        return

    actor_folder = ",".join(map(lambda i: i.name, meta.actors[0:3])) + ("等" if len(meta.actors) > 3 else "")
    video_folder = f'{meta.num}-{meta.title}'

    save_path = os.path.join(output_path, actor_folder, video_folder)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    image_extension = image.save_images(meta.cover, number, save_path)
    logger.info("图片生成成功!")

    nfo_generator.generate(meta, number.file_name, image_extension, save_path)
    logger.info("NFO文件生成成功!")

    save_file = os.path.join(save_path, f'{number.file_name}.{number.extension}')
    if os.path.exists(save_file) and os.stat(save_file).st_size == os.stat(path).st_size:
        logger.info("影片文件已存在且大小相同，已跳过复制!")
        return

    logger.info("开始复制影片...")
    shutil.copy2(path, save_file)
    logger.info("影片复制成功!")


if __name__ == '__main__':
    run()
