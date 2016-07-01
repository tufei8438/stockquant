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
import decimal
import time
import datetime
import threading

from stockquant.database.models import Trade, Company
from stockquant.database.services import TradeService
from stockquant.spider import Spider, SpiderError
from stockquant.utils.holiday import Holiday
from stockquant.utils.log import logger


class StockMiniuteQueryParser(object):

    _today = None

    def __init__(self, stock_code, data):
        assert isinstance(data, dict)
        self._stock_code = stock_code
        self._data = data
        self._trades = []

        if not self._data.has_key('data'):
            raise SpiderError("invalid data:%s" % self._data)
        stock_code_data = self._data.get('data').get(stock_code)
        if not stock_code_data:
            raise SpiderError("invalid data:%s" % self._data)

        try:
            mx_data = stock_code_data['mx_price']['mx']['data'][1]
            self._trades = self.parse_many(self._stock_code, mx_data)
        except (KeyError, IndexError):
            self._trades = []

    @classmethod
    def parse_many(cls, stock_code, data):
        cls._today = datetime.datetime.now()
        trades = []
        array = data.split('|')
        for item in array:
            trades.append(cls.parse(stock_code, item))
        cls._today = None
        return trades

    @classmethod
    def parse(cls, stock_code, text):
        array = text.split('/')
        if len(array) != 7:
            raise SpiderError("parse TradeDetail error. invalid text:" + text)
        trade = Trade(stock_code=stock_code)
        trade.trade_time = cls._get_trade_time(array[1])
        trade.trade_price = decimal.Decimal(array[2])
        trade.price_change = decimal.Decimal(array[3])
        trade.volume = int(array[4])
        trade.amount = int(array[5])
        trade.nature = array[6]
        return trade

    @classmethod
    def _get_trade_time(cls, time_text):
        datetime_text = cls._today.strftime("%Y-%m-%d ") + time_text
        return datetime.datetime.strptime(datetime_text, "%Y-%m-%d %H:%M:%S")

    @property
    def trades(self):
        return self._trades


class StockCompanyQueryParser(object):

    def __init__(self, stock_code, data):
        assert isinstance(data, dict)
        self._stock_code = stock_code
        self._data = data

        company = Company()
        gegu = self._data['data']['gegu']
        company.stock_code = self._stock_code
        company.name = gegu.get('gsmz')
        riqi = gegu.get('riqi')
        company.listing_date = riqi and datetime.datetime.strptime(riqi, '%Y-%m-%d') or None
        jg = gegu.get('jg')
        company.issue_price = jg and decimal.Decimal(jg) or None
        fxs = gegu.get('fxs')
        if fxs:
            company.issue_number = int(float(fxs.replace('万股', '')) * 10000)
        company.local_area = gegu.get('dy')
        company.business_scope = gegu.get('yw')

        plate = gegu.get('plate')
        company.industry_code = plate[0]['id']
        company.industry_name = plate[0]['name']

        self._company = company

    @property
    def company(self):
        return self._company


class TencentSpider(Spider):

    STOCK_MINUTE_QUERY_URL = 'http://proxy.finance.qq.com/ifzqgtimg/appstock/app/minute/query'
    STOCK_COMPANY_QUERY_URL = 'http://proxy.finance.qq.com/ifzqgtimg/stock/corp/cwbb/search'

    def query_stock_minute(self, stock_code):
        parameters = {
            'p': 1,
            'code': stock_code,
            '_rndtime': int(time.time())
        }
        data = self.fetch('GET', self.STOCK_MINUTE_QUERY_URL, params=parameters)
        return StockMiniuteQueryParser(stock_code, data).trades

    def query_company(self, stock_code):
        parameters = {
            'symbol': stock_code,
            'type': 'sum',
            'num': 4,
            'jianjie': 1,
            '_rndtime': int(time.time()),
        }
        data = self.fetch('GET', self.STOCK_COMPANY_QUERY_URL, params=parameters)
        return StockCompanyQueryParser(stock_code, data).company


class TencentRunner(threading.Thread):

    _trade_start_am = '09:25'
    _trade_end_am = '11:31'
    _trade_start_pm = '12:59'
    _trade_end_pm = '15:01'

    def __init__(self, stock_code, interval, callback):
        super(TencentRunner, self).__init__()
        assert callable(callback)
        self._interval = interval
        self._stock_code = stock_code
        self._callback = callback
        self._running = True

    def run(self):
        while self._running:
            try:
                self._run()
                time.sleep(self._interval)
            except Exception:
                logger.exception("运行TencentRunner异常")

    def _run(self):
        if not self._in_trading():
            return

        trades = TencentSpider().query_stock_minute(self._stock_code)
        with TradeService() as trade_service:
            db_trades = trade_service.query_trades(stock_code=self._stock_code, limit=100)
            for trade in trades:
                if trade not in db_trades:
                    trade_service.add_trade(trade)
                    self._callback(trade)

    @classmethod
    def _get_trade_datetime(cls, time_text, today=None):
        if today is None:
            today = datetime.datetime.now()
        datetime_text = today.strftime("%Y-%m-%d ") + time_text
        return datetime.datetime.strptime(datetime_text, '%Y-%m-%d %H:%M')

    def _in_trading(self):
        """ 判断当前时间是否为交易时间
        :return: bool
        """
        today = datetime.datetime.now()
        if today.weekday() == 6 or today.weekday() == 0:
            return False
        if Holiday.is_holiday(today):
            return False

        am_start_time = self._get_trade_datetime(self._trade_start_am, today)
        am_end_time = self._get_trade_datetime(self._trade_end_am, today)
        pm_start_time = self._get_trade_datetime(self._trade_start_pm, today)
        pm_end_time = self._get_trade_datetime(self._trade_end_pm, today)

        if am_start_time < today < am_end_time or pm_start_time < today < pm_end_time:
            return True
        else:
            return False

    def stop(self):
        self._running = False
