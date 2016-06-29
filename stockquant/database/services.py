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
from sqlalchemy.orm import sessionmaker
from stockquant.database import engine
from stockquant.database.models import Trade


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


class TradeService(BaseService):

    def add_trade(self, trade):
        self._db.add(trade)

    def query_trades(self, stock_code, limit=0):
        """根据股票代码查询最近交易记录
        :param stock_code:
        :param limit: 为0时返回所有记录, 大于0则返回给定的记录数
        :return: 交易列表
        """
        q = self._db.query(Trade).filter(Trade.stock_code == stock_code).order_by(Trade.trade_time.desc())
        if limit:
            q = q.limit(limit)
        return q.all()