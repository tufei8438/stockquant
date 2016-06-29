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
import decimal

from stockquant.database.models import Trade
from stockquant.database.services import TradeService


class TradeTest(unittest.TestCase):

    def test_eq(self):
        with TradeService() as trade_service:
            db_trades = trade_service.query_trades('sz002177')

            trade = Trade()
            trade.stock_code = 'sz002177'
            trade.trade_time = datetime.datetime.strptime('2016-06-27 14:56:07', '%Y-%m-%d %H:%M:%S')
            trade.trade_price = decimal.Decimal('9.51')
            trade.price_change = decimal.Decimal('0.00')
            trade.volume = 220
            trade.amount = 209435
            trade.nature = 'S'

            self.assertEqual(trade, db_trades[0])
