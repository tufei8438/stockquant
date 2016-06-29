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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL

Base = declarative_base()


class Trade(Base):

    __tablename__ = 'trade'

    id = Column(Integer, primary_key=True)
    stock_code = Column(String(32))
    trade_time = Column(TIMESTAMP)
    trade_price = Column(DECIMAL)
    price_change = Column(DECIMAL)
    volume = Column(Integer)
    amount = Column(Integer)
    nature = Column(String(32))

    def __eq__(self, other):
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

    def __hash__(self):
        return hash(self.stock_code) ^ \
               hash(self.trade_time) ^ \
               hash(self.trade_price) ^ \
               hash(self.price_change) ^ \
               hash(self.volume) ^ \
               hash(self.amount) ^ \
               hash(self.nature)
