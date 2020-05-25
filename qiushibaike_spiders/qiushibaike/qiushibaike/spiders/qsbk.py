# -*- coding: utf-8 -*-
import scrapy
from qiushibaike.items import QiushibaikeItem

class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']

    def parse(self, response):
        print(response.url)
        div_list = response.xpath("//div[contains(@class,'article block')]")
        for div in div_list:
            item = QiushibaikeItem()
            item['name'] = div.xpath("//h2/text()").extract_first()
            item['sex'] = div.xpath("//div[contains(@class,'Icon')]/@class").extract_first()
            item['subs'] = div.xpath("//span[@class='stats-vote']/i/text()").extract_first()
            item['comment'] = div.xpath("//span[@class='stats-comments']//i/text()").extract_first()
            yield item

        page = response.url.split('/')[5]
        if int(page)<13:
            new_page = int(page)+1
            new_page = str(new_page)
            next_url = response.url.replace(page,new_page)
            yield scrapy.Request(next_url,callback=self.parse)

