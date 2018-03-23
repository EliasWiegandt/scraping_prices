# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WuptiSpider(scrapy.Spider):
    name = 'wupti_prices'
    allowed_domains = ['wupti.com', 'wupti.dk']
    start_urls = ['https://www.wupti.com/produkter/hvidevarer/koel-og-frys/']
    # start_urls = [
    #     'https://www.wupti.com/produkter/hvidevarer/koel-og-frys/koele/fryseskabe/siemens-kg39ebi40-taenk-bedst'
    # ]

    products = lf.load_names()
    product_url = [product.lower() for product in products]

    rules = (
        Rule(LinkExtractor(allow=(product_url)), callback='parse_item'),
        Rule(LinkExtractor(allow=r"koele")),
    )

    def parse_item(self, response):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        for product in self.products:
            if product.lower() in response.request.url:
                product_match = product
        p = ProductLoader(item=Product(), response=response)
        p.add_value('product', product_match)

        normal_div = '//div[@class="seller seller-first"]//div[@class="productPrice nobefore"]//strong/text()'
        discount_div = '//div[@class="seller seller-first"]//div[@class="productPrice"]//strong/text()'
        normal_container = response.xpath(normal_div)
        discount_container = response.xpath(discount_div)

        if len(discount_container) > 0:
            price_div = discount_div
        else:
            price_div = normal_div

        print('============================')
        print(normal_container)
        print(discount_container)
        print('============================')

        p.add_xpath('price', price_div)
        p.add_value('date', date)
        p.add_value('retailer', "Wupti")
        yield p.load_item()

        w = WebsiteLoader(item=Website(), response=response)
        w.add_value('html', response.body)
        w.add_value('date', date)
        w.add_value('product', product_match)
        w.add_value('retailer', "Wupti")
        yield w.load_item()
