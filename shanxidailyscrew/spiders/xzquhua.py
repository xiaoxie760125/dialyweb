# -*- coding: utf-8 -*-
import scrapy
from  scrapy import  Selector
from  scrapy.http import Request,Response
from shanxidaily import  items
from  urllib.parse import  urljoin
class XzquhuaSpider(scrapy.Spider):
    name = 'xzquhua'
    allowed_domains = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/61/6105.html']

    def parse(self, response):
        res=Selector(response)
        print(response.text)
        href=res.css('.provincetr td a::attr(href)')
        print(len(href))
        for f in href.extract():
            url=urljoin(response.url,f)
            yield  Request(url=url,callback=self.nextparse)



    def  nextparse(self,response):
        print(response.text)
        res = Selector(response)
        href=res.css('tr')
        for h in href:
            a=href.css('a')
            if a:
                cityitem=items.ShanxidailyItem()
                cityitem.susdepcode=a[0].css('::text').extract()
                cityitem.susdepname=a[1].css('::text').extract()
                yield  cityitem

                href=a[0].css('::attr(href)').extract()
                url = urljoin(response.url, href)
                print(url)
                yield Request(url=url,callback=self.nextparse)



