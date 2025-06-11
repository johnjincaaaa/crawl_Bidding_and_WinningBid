# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class JiangxiCnPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.client['江西公共资源每日招标信息']
        self.collection = None

    def process_item(self, item, spider):
        a = item.get('name')
        self.collection = self.db[a]
        print(item,'看着这里')
        self.collection.insert_one(dict(item))
        return item

    def __del__(self):
        self.client.close()


class JiangxiWinPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.client['江西公共资源每日中标信息']
        self.collection = None

    def process_item(self, item, spider):
        a = item.get('name')
        self.collection = self.db[a]
        self.collection.insert_one(dict(item))
        return item

    def __del__(self):
        self.client.close()