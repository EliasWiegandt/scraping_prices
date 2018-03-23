# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
import csv
from pricebot.items import Link, LinkLoader
import pyhelpers.loadfuncs as lf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time


class PowerLinksSpider(scrapy.Spider):
    name = 'power_links'
    allowed_domains = ['www.power.dk']
    start_urls = ['https://www.power.dk']

    # driver = webdriver.Firefox()
    options = webdriver.ChromeOptions()
    WINDOW_SIZE = "1920,1080"
    options.add_argument("--headless")
    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # options.add_argument("--start-maximized")
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe", chrome_options=options)
    products = lf.load_names()
    # products = ['KGE36BI40']

    def parse(self, response):
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
                    '//div[@class="product product-element angi product-4col"]')
                link = str(link_container.get_attribute("data-gtmurl"))
                product_link = 'https://www.punkt1.dk' + link
                l = LinkLoader(item=Link())
                l.add_value('link', product_link)
                l.add_value('product', product)
                l.add_value('date', date)
                l.add_value('retailer', 'Power')
                yield l.load_item()
            except NoSuchElementException:
                print(" ")
                print("-----------------------------")
                print("Element does not exist")
                print("-----------------------------")
                print(" ")
        self.driver.close()
