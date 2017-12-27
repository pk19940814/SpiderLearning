# -*- coding: utf-8 -*-


from scrapy.exceptions import DropItem


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
