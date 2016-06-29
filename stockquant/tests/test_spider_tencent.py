# coding:utf8

"""
Copyright 2016 Smallpay Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
from stockquant.spider.tencent import TencentSpider, TencentRunner


class TencentSpiderTest(unittest.TestCase):

    def test_query_stock_minute(self):
        spider = TencentSpider()
        trade_details = spider.query_stock_minute('sz002177')
        for trade_detail in trade_details:
            print trade_detail
        self.assertEqual(len(trade_details), 20)

        import time
        time.sleep(20)
        trade_details_n = spider.query_stock_minute('sz002177')

        l = trade_details + trade_details_n

        print '\n\n'
        td_set = set(l)
        for t in td_set:
            print t
        self.assertEqual(len(td_set), 20)


def tencent_runner_callback(trade):
    print 'Get trade price:%s' % trade.trade_price


class TencentRunnerTest(unittest.TestCase):

    def test_run(self):
        runner = TencentRunner('sz002177', 5, tencent_runner_callback)
        runner.start()