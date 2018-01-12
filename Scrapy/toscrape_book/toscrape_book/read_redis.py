#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : read_redis.py
# @Author: Kom
# @Date  : 2018/1/12
# @Desc  :

import redis
import json

ITEM_KEY = 'books:items'


def process_item(item):
    pass


def main():
    r = redis.StrictRedis(host='127.0.0.1', port=7369)
    for _ in range(r.llen(ITEM_KEY)):
        data = r.lpop(ITEM_KEY)
        item = json.loads(data.decode('utf8'))
        process_item(item)


if __name__ == '__main__':
    main()
