# -*- coding: utf-8 -*-


from scrapy.exceptions import DropItem
from scrapy.item import Item
import pymongo


class PriceConverterPipeline(object):
    # 英镑兑换人民币的汇率
    exchange_rate = 8.5309

    def process_item(self, item, spider):
        # 提取item的price字段
        # 去掉前面英镑符号，转换为float类型，乘以汇率
        price = float(item['price'][1:]) * self.exchange_rate

        # 保留2位小数，赋值回item的price字段

        item['price'] = '￥%.2f' % price

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['name']
        if name in self.book_set:
            raise DropItem("Duplicate book found: %s" & item)

        self.book_set.add(name)
        return item


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URI = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017/')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_data')
        return cls()

    def __init__(self):
        self.client = None
        self.db = None

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URI)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        return item


if __name__ == "__main__":
    mongopipeline = MongoDBPipeline()
    mongopipeline.open_spider(None)
    mongopipeline.close_spider(None)
