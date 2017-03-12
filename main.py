# coding=utf-8

from spider import Spider

import sys

class Main(object):
    @staticmethod
    def main():
        reload(sys)
        sys.setdefaultencoding('utf8')
        spider = Spider('python','杭州')
        spider.setSalay(5.9,16,10.9,31.0)
        spider.addShieldCompany('畅唐网络')
        spider.addShieldCompany('中国亿教亿学网')
        spider.addContainText('C++')
        spider.addContainText('c++')
        #spider.addContainText('爬虫')
        spider.analyse()

Main.main()
