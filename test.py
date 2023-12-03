import unittest

from spider.dmm import DmmSpider
from spider.jav321 import Jav321Spider


class SpiderTest(unittest.TestCase):
    def testJav321(self):
        Jav321Spider("SIVR-298").get_info()

    def testDmm(self):
        DmmSpider("SIVR-298").get_info()


if __name__ == '__main__':
    unittest.main()
