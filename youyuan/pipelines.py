# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.conf import settings
from pymongo import MongoClient


# class jsonfilePipeline(object):
#     def process_item(self, item, spider):
#         with codecs.open('yy.json', 'a', encoding='utf-8') as f:
#             jsontext = json.dumps(dict(item), ensure_ascii=False) + '\n'
#             f.write(jsontext)
#             return item


class mongoPipeline(object):
    def process_item(self, item, spider):
        client = MongoClient(host=settings['host'], port=settings['port'])
        dbname = settings['DBNAME']
        collname = settings['COLLNAME']
        coll = client[dbname][collname]
        coll.insert(dict(item))
        client.close()
        return item