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
import datetime

from stockquant.database.models import Trade
from stockquant.strategy.blocktrading import BlockTradingStrategy
from stockquant.utils.mail import Mail


class BlockTradingStrategyTest(unittest.TestCase):

    def test_mail_content(self):
        trade = Trade(stock_code='sz002177', trade_time=datetime.datetime.now())
        strategy = BlockTradingStrategy(trade)
        content = strategy.get_mail_content()
        print content

        Mail().send('股票账号交易行情', content, subtype='html')