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
import datetime
from sqlalchemy.orm import sessionmaker
from stockquant.database import engine
from stockquant.database.models import Trade, Company


class BaseService(object):

    __Session = sessionmaker(bind=engine)

    def __enter__(self):
        self._db = self.__Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_type, BaseException):
            self._db.rollback()
        else:
            self._db.commit()
        self._db.close()

    def flush(self):
        self._db.flush()


class TradeService(BaseService):

    def add_trade(self, trade):
        self._db.add(trade)
        self.flush()

    def get_trade(self, trade_id):
        return self._db.query(Trade).filter(Trade.trade_id == trade_id).first()

    def query_trades(self, stock_code, limit=0, trade_time=None):
        """根据股票代码查询最近交易记录
        :param stock_code: 股票代码
        :param limit: 为0时返回所有记录, 大于0则返回给定的记录数
        :param trade_time:
        :return: 交易列表
        """
        q = self._db.query(Trade).filter(Trade.stock_code == stock_code).order_by(Trade.trade_time.desc())
        if limit:
            q = q.limit(limit)
        if trade_time:
            if isinstance(trade_time, datetime.datetime):
                p_trade_time = trade_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                p_trade_time = trade_time
            q = q.filter(Trade.trade_time >= p_trade_time)
        return q.all()

    def get_last_trade_time(self, stock_code):
        trade = self._db.query(Trade).filter(Trade.stock_code == stock_code).\
            order_by(Trade.trade_time.desc()).first()
        return trade.trade_time if trade else None


class CompanyService(BaseService):

    def add_company(self, company):
        self._db.add(company)
        self.flush()

    def get_company(self, stock_code):
        return self._db.query(Company).filter(Company.stock_code == stock_code).fitst()

    def query_companies(self):
        return self._db.query(Company).all()