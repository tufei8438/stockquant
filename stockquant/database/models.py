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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATETIME, DECIMAL, DATE, BIGINT

Base = declarative_base()


class Trade(Base):

    __tablename__ = 'trade'

    id = Column(Integer, primary_key=True)
    stock_code = Column(String(32))
    trade_seq = Column(Integer)
    trade_time = Column(DATETIME)
    trade_price = Column(DECIMAL)
    price_change = Column(DECIMAL)
    volume = Column(Integer)
    amount = Column(Integer)
    nature = Column(String(32))

    def equal(self, other):
        if not isinstance(other, Trade):
            return False
        if self.stock_code == other.stock_code \
            and self.trade_time == other.trade_time \
            and self.trade_price == other.trade_price \
            and self.price_change == other.price_change \
            and self.volume == other.volume \
            and self.amount == other.amount \
            and self.nature == other.nature:
            return True
        else:
            return False

    @classmethod
    def minus(cls, trades, other_trades):
        if not other_trades:
            return trades

        same_trades = []
        for trade in trades:
            for o_trade in other_trades:
                if trade.equal(o_trade):
                    same_trades.append(trade)
        return list(set(trades).difference(set(same_trades)))


class Company(Base):

    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    stock_code = Column(String(32))
    name = Column(String(64))
    listing_date = Column(DATE, nullable=True)
    issue_price = Column(DECIMAL, nullable=True)
    issue_number = Column(BIGINT, nullable=True)
    business_scope = Column(String(1024), nullable=True)
    industry_code = Column(String(16))
    industry_name = Column(String(32))
    local_area = Column(String(32), nullable=True)