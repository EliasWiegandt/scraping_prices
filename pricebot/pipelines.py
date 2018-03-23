# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
import datetime
import os


class HtmlFilePipeline(object):
    def open_spider(self, spider):
        now = datetime.datetime.now()
        self.date = now.strftime("%Y%m%d")

    def process_item(self, item, spider):
        if 'html' in item:
            product = item['product']
            retailer = spider.name.split('_')[0]
            filename = os.path.join(os.getcwd(),
                                    'websitehistory/%s/%s_%s_%s.html' %
                                    (retailer, retailer, self.date, product))
            file = open(filename, 'wb')
            with file as f:
                f.write(item['html'])
                f.close()
        return item


class ProductPipeline(object):
    def open_spider(self, spider):
        if 'prices' in spider.name:
            now = datetime.datetime.now()
            date = now.strftime("%Y%m%d")
            retailer = spider.name.split('_')[0]
            filename = os.path.join(os.getcwd(), 'pricedata/%s/%s_%s.csv' %
                                    (retailer, retailer, date))
            self.file = open(filename, 'wb')
            self.exporter = CsvItemExporter(self.file)
            self.exporter.fields_to_export = [
                'date', 'retailer', 'product', 'price'
            ]
            self.exporter.start_exporting()

    def close_spider(self, spider):
        if 'prices' in spider.name:
            self.exporter.finish_exporting()
            self.file.close()

    def process_item(self, item, spider):
        if 'price' in item:
            self.exporter.export_item(item)
        return item
