# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from pricebot.items import Product, ProductLoader, Website, WebsiteLoader
import pyhelpers.loadfuncs as lf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class Punkt1Spider(scrapy.Spider):

    name = 'punkt1_prices'
    allowed_domains = ['punkt1.dk', 'punkt1.com']
    start_urls = ['https://www.punkt1.dk']

    options = webdriver.ChromeOptions()
    WINDOW_SIZE = "1920,1080"
    options.add_argument("--headless")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        executable_path=r"chromedriver.exe", chrome_options=options)
    products = lf.load_names()

    # products = ['KGE36BW40', 'KG49EBI40']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        url = response.request.url
        links_list = []
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        self.driver.get(response.url)

        for product in self.products:
            search_form = self.driver.find_element_by_id('search-input')
            search_form.send_keys(product)
            time.sleep(1.0)
            search_button = self.driver.find_element_by_id('search-button')
            search_button.click()
            time.sleep(1.0)
            try:
                link_container = self.driver.find_element_by_xpath(
                    '//div[@class="product product-element angi product-4col"]'
                )
                link_ext = str(link_container.get_attribute("data-gtmurl"))
                link_all = self.start_urls[0] + link_ext
                yield scrapy.Request(
                    url=link_all, callback=self.parse_product_page)
            except NoSuchElementException:
                continue
        self.driver.close()

    def parse_product_page(self, response):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        for product in self.products:
            if product.lower() in response.request.url:
                product_match = product
                p = ProductLoader(item=Product(), response=response)
                p.add_value('product', product_match)

                normal_div = '//span[@class="product-price-tag"]/text()'
                discount_div = '//span[@class="product-price-tag"]/text()'
                normal_container = response.xpath(normal_div)
                discount_container = response.xpath(discount_div)

                if len(discount_container) > 0:
                    price_div = discount_div
                else:
                    price_div = normal_div

                p.add_xpath('price', price_div)
                p.add_value('date', date)
                p.add_value('retailer', "Punkt1")
                yield p.load_item()

                w = WebsiteLoader(item=Website(), response=response)
                w.add_value('html', response.body)
                w.add_value('date', date)
                w.add_value('product', product_match)
                w.add_value('retailer', "Punkt1")
                yield w.load_item()
