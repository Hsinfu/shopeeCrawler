#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from shopee import ShopeeAPI

logger = logging.getLogger(__name__)
logfile = "/tmp/shopeeCrawler.run.py.log"


def main():
    shopee_api = ShopeeAPI()
    payload = {
        'is_massship': False,
        'limit': 40,
        'offset': 0,
        'search': '',
        'type': '',
    }
    res = shopee_api.get(url='https://seller.shopee.tw/api/v1/orders/', params=payload)
    print(res)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(relativeCreated)6d %(threadName)s %(message)s',
        filename=logfile,
        filemode='w')
    main()
