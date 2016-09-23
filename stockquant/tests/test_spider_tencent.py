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


mx = "1850/09:45:12/9.72/-0.01/146/141893/S|1855/09:45:15/9.72/0.00/5/4860/B|1858/09:45:18/9.72/0.00/280/272312/B|1864/09:45:18/9.71/-0.01/78/75746/S|1870/09:45:24/9.72/0.01/5/4860/B|1874/09:45:27/9.72/0.00/4/3888/B|1879/09:45:27/9.72/0.00/161/156445/S|1884/09:45:33/9.72/0.00/11/10694/B|1888/09:45:33/9.72/0.00/48/46654/S|1890/09:45:36/9.72/0.00/66/64115/S|1896/09:45:39/9.72/0.00/35/34020/B|1901/09:45:42/9.72/0.00/148/143866/B|1905/09:45:48/9.72/0.00/5/4860/S|1908/09:45:51/9.72/0.00/20/19440/S|1915/09:45:54/9.73/0.01/11/10697/B|1918/09:45:54/9.72/-0.01/278/270216/S|1927/09:46:00/9.72/0.00/164/159399/S|1930/09:46:03/9.72/0.00/45/43740/B|1934/09:46:03/9.72/0.00/124/120538/B|1938/09:46:06/9.71/-0.01/102/99131/S"
mx_1 = "1832/09:44:57/9.73/0.01/169/164339/B|1835/09:45:03/9.72/-0.01/52/50549/S|1840/09:45:06/9.73/0.01/34/33082/B|1845/09:45:09/9.73/0.00/86/83661/B|1850/09:45:12/9.72/-0.01/146/141893/S|1855/09:45:15/9.72/0.00/5/4860/B|1858/09:45:18/9.72/0.00/280/272312/B|1864/09:45:18/9.71/-0.01/78/75746/S|1870/09:45:24/9.72/0.01/5/4860/B|1874/09:45:27/9.72/0.00/4/3888/B|1879/09:45:27/9.72/0.00/161/156445/S|1884/09:45:33/9.72/0.00/11/10694/B|1888/09:45:33/9.72/0.00/48/46654/S|1890/09:45:36/9.72/0.00/66/64115/S|1896/09:45:39/9.72/0.00/35/34020/B|1901/09:45:42/9.72/0.00/148/143866/B|1905/09:45:48/9.72/0.00/5/4860/S|1908/09:45:51/9.72/0.00/20/19440/S|1915/09:45:54/9.73/0.01/11/10697/B|1918/09:45:54/9.72/-0.01/278/270216/S"

class Test(unittest.TestCase):

    def test_gu(self):
        from stockquant.database.models import Trade
        from stockquant.spider.tencent import StockMiniuteQueryParser
        trades = StockMiniuteQueryParser.parse_many('sz002177', mx)
        trades_1 = StockMiniuteQueryParser.parse_many('sz002177', mx_1)

        for trade in trades:
            for trade_1 in trades_1:
                if trade_1 == trade:
                    print trade.__dict__