# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from youyuan.items import YouyuanItem
import re


class YySpider(RedisSpider):
    name = 'yy'
    allowed_domains = ['www.95195.com']
    start_urls = ['http://www.95195.com/index/default/0/1/1.html']

    def parse(self, response):
        page = re.search('/(\d+)\.html', response.url)
        if page:
            page = page.group(1)
        links = response.xpath('//a[@class="oimgbg"]')
        for link in links:
            url = link.xpath('./@href').extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.parse1)
        if int(page) < 7:
            page = int(page) + 1
            next_url = 'http://www.95195.com/index/default/0/1/' + str(page) + '.html'
            yield scrapy.Request(next_url, callback=self.parse)

    def parse1(self, response):
        item = YouyuanItem()
        item['picture'] = response.xpath('//img[@id="changesize"]/@src').extract()
        item['name'] = response.xpath('//b[@class="corred"]/text()').extract_first()
        yield item


if __name__ == '__main__':
    cmdline.execute('scrapy crawl yy'.split())
