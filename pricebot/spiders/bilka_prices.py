# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf


class BilkaSpider(scrapy.Spider):
    name = 'bilka_prices'
    allowed_domains = ['hvidevarer.bilka.dk']

    def __init__(self):
        self.products = lf.load_names()
        # self.products = ['KG49EBI40']
        self.url_base = 'https://hvidevarer.bilka.dk'
        self.url_before = 'https://hvidevarer.bilka.dk/search?searchText='
        self.url_end = ''

    def start_requests(self):
        for product in self.products:
            url = self.url_before + product + self.url_end
            yield scrapy.Request(url=url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        search_container = response.xpath('//a[@class="productPhotoLink"]')
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
        for product in self.products:
            if product.lower() in response.request.url:
                product_match = product
                normal_div = '//div[@class="priceAndAvail"]//div[@class="productPrice nobefore"]//strong/text()'
                discount_div = '//div[@class="priceAndAvail"]//div[@class="productPrice"]//strong/text()'
                normal_container = response.xpath(normal_div)
                discount_container = response.xpath(discount_div)

                if len(discount_container) > 0:
                    price_div = discount_div
                else:
                    price_div = normal_div

                # print('============================')
                # print(normal_container)
                # print(discount_container)
                # print('============================')

                p = ProductLoader(item=Product(), response=response)
                p.add_value('product', product_match)

                p.add_xpath('price', price_div)
                p.add_value('date', date)
                p.add_value('retailer', "Bilka")
                yield p.load_item()

                w = WebsiteLoader(item=Website(), response=response)
                w.add_value('html', response.body)
                w.add_value('date', date)
                w.add_value('product', product_match)
                w.add_value('retailer', "Bilka")
                yield w.load_item()
