# coding=utf-8

from spider import Spider
from file import File

import sys

class Main(object):
    @staticmethod
    def main():
        reload(sys)
        sys.setdefaultencoding('utf8')
        spider = Spider('python','杭州')
        spider.setSalay(5.9,16,10.9,31.0)
        spider.analyse()

Main.main()
