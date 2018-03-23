# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf


class WhiteawaySpider(scrapy.Spider):
    name = 'whiteaway_prices'
    allowed_domains = ['whiteaway.com']
    products = lf.load_names()
    # self.products = ['KGE36BI40']
    url_base = 'https://www.whiteaway.com'
    url_before = 'https://www.whiteaway.com/search_result/?keywords='
    url_end = '#/'

    def start_requests(self):
        for product in self.products:
            url = self.url_before + product + self.url_end
            yield scrapy.Request(url=url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        search_container = response.xpath('//a[@class="srp__product-link"]')
        if len(search_container) > 0:
            url_add = search_container.xpath('@href').extract_first()
            url = self.url_base + url_add
            yield scrapy.Request(url=url, callback=self.parse_product_page)
        else:
            for product in self.products:
                if product.lower() in response.request.url:
                    product_match = product
            print(' ')
            print('------------------------------------')
            print(product_match, " not found")
            print('------------------------------------')
            print(' ')

    def parse_product_page(self, response):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        product_match = 'unkown'
        for product in self.products:
            if product.lower() in response.request.url:
                product_match = product

                p = ProductLoader(item=Product(), response=response)
                p.add_value('product', product_match)

                p.add_xpath('price',
                            '//div[@class="vip__price-box-price"]/text()')
                p.add_value('date', date)
                p.add_value('retailer', "Whiteaway")
                yield p.load_item()

                w = WebsiteLoader(item=Website(), response=response)
                w.add_value('html', response.body)
                w.add_value('date', date)
                w.add_value('product', product_match)
                w.add_value('retailer', "Whiteaway")
                yield w.load_item()
