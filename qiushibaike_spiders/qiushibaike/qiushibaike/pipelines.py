# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

client = MongoClient(host="127.0.0.1", port=27017)
collection = client["my_test"]["scrapy_qsbk"]

class QiushibaikePipeline(object):
    def process_item(self, item, spider):
        collection.insert_one(dict(item))
