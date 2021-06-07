import scrapy
from DataSpider.items import RealTimeHotItem
import time
import datetime


class WeibospiderSpider(scrapy.Spider):
    name = 'weiboSpider'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/top/summary?cate=realtimehot',
                  # 'https://s.weibo.com/top/summary?cate=socialevent'
                  ]

    def parse(self, response):
        if response.url == self.start_urls[0]:
            yield scrapy.Request(
                url=response.url,
                callback=self.parse_realtimehot,
            )
        # if response.url == self.start_urls[1]:
        #     yield scrapy.Request(
        #         url=response.url,
        #         callback=self.parse_socialevent,
        #     )

    def parse_realtimehot(self, response):
        for res in response.xpath("//tbody/tr"):
            item = RealTimeHotItem()
            srank = res.xpath("td[1]/text()").extract_first() if res.xpath("td[1]/text()").extract_first() else 0
            title = res.xpath("td[2]/a/text()").extract_first()
            heat = res.xpath("td[2]/span/text()").extract_first() if res.xpath("td[2]/span/text()") else ''
            tag = res.xpath("td[3]/i/text()").extract_first() if res.xpath("td[3]/i/text()").extract_first() else ''
            href = res.xpath("td[2]/a/@href").extract_first() if res.xpath(
                "td[2]/a/@href").extract_first() != "javascript:void(0);" else res.xpath(
                "td[2]/a/@href_to").extract_first()
            item['srank'] = srank
            item['title'] = title
            item['heat'] = heat
            item['tag'] = tag
            item['href'] = href
            item['datetime'] = datetime.datetime(
                int(time.strftime('%Y', time.localtime(time.time()))),
                int(time.strftime('%m', time.localtime(time.time()))),
                int(time.strftime('%d', time.localtime(time.time()))),
                int(time.strftime('%H', time.localtime(time.time()))),
                int(time.strftime('%M', time.localtime(time.time()))),
                int(time.strftime('%S', time.localtime(time.time()))),
            )
            if tag == '荐':
                del item['title']
                del item['heat']
                del item['href']
                yield item
            else:
                yield item

    # def parse_socialevent(self, response):
    #     for res in response.xpath("//tbody/tr"):
    #         item = SocialEventItem()
    #         title = res.xpath("td[2]/a/text()").extract_first()
    #         href = res.xpath("td[2]/a/@href").extract_first() if res.xpath(
    #             "td[2]/a/@href").extract_first() != "javascript:void(0);" else res.xpath(
    #             "td[2]/a/@href_to").extract_first()
    #         item['title'] = title
    #         item['href'] = href
    #         item['datetime'] = datetime.datetime(
    #             int(time.strftime('%Y', time.localtime(time.time()))),
    #             int(time.strftime('%m', time.localtime(time.time()))),
    #             int(time.strftime('%d', time.localtime(time.time()))),
    #             int(time.strftime('%H', time.localtime(time.time()))),
    #             int(time.strftime('%M', time.localtime(time.time()))),
    #             int(time.strftime('%S', time.localtime(time.time()))),
    #         )
    #         yield item
