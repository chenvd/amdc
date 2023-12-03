from spider.spider_exception import SpiderException
from utils.logger import logger


class Spider:
    name = None

    def __init__(self, num):
        self.num = num

    def get_info(self):
        pass

    def combine(*spiders):
        metas = []
        for spider in spiders:
            try:
                logger.info(f"站点《{spider.name}》开始获取...")
                meta = spider.get_info()
                metas.append(meta)
                logger.info(f"站点《{spider.name}》获取成功!")
            except SpiderException as e:
                logger.info(f"站点《{spider.name}》获取失败：{e.message}，已跳过!!!")
            except Exception as e:
                logger.error(f'站点《{spider.name}》获取失败，已跳过!!!', exc_info=True)

        if len(metas) == 0:
            return

        meta = metas[0]
        if len(metas) >= 2:
            for key in meta.__dict__:
                if getattr(meta, key) is None:
                    for other_meta in metas[1:]:
                        value = getattr(other_meta, key)
                        if value:
                            setattr(meta, key, value)
                            break
            logger.info("站点信息合并完成！")
        return meta
