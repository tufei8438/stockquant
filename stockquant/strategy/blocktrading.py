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
from jinja2 import Template
from stockquant.database.services import TradeService
from stockquant.strategy import Strategy
from stockquant.utils.mail import Mail

# 邮件模板见http://nec.netease.com/framework/html-email.html
MAIL_CONTENT_TEMPLATE = """
<div style="text-align:center;">
    <table width="600" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;"><tbody><tr><td>
        <div style="width:600px;text-align:left;font:12px/15px simsun;color:#000;background:#fff;">
            <table border="1" cellpadding="10">
               <caption>交易详情</caption>
               <thead>
                  <tr>
                     <th>股票代码</th>
                     <th>交易时间</th>
                     <th>交易价格</th>
                     <th>价格变动</th>
                     <th>交易笔数</th>
                     <th>交易金额</th>
                     <th>交易标示</th>
                  </tr>
               </thead>
               <tbody>
                  <tr>
                     <td>{{ trade.stock_code }}</td>
                     <td>{{ trade.trade_time.strftime('%H:%M:%S') }}</td>
                     <td>{{ trade.trade_price }}</td>
                     <td>{{ trade.price_change }}</td>
                     <td>{{ trade.volume }}</td>
                     <td>{{ trade.amount }}</td>
                     <td>{{ trade.nature }}</td>
                  </tr>
               </tbody>
            </table>
            <table border="1" cellpadding="10">
               <caption>最近10笔的交易</caption>
               <thead>
                  <tr>
                     <th>股票代码</th>
                     <th>交易时间</th>
                     <th>交易价格</th>
                     <th>价格变动</th>
                     <th>交易笔数</th>
                     <th>交易金额</th>
                     <th>交易标示</th>
                  </tr>
               </thead>
               <tbody>
               {% for trade in db_trades %}
                  <tr>
                     <td>{{ trade.stock_code }}</td>
                     <td>{{ trade.trade_time.strftime('%H:%M:%S') }}</td>
                     <td>{{ trade.trade_price }}</td>
                     <td>{{ trade.price_change }}</td>
                     <td>{{ trade.volume }}</td>
                     <td>{{ trade.amount }}</td>
                     <td>{{ trade.nature }}</td>
                  </tr>
                {% endfor %}
               </tbody>
            </table>
        </div>
    </td></tr></tbody></table>
</div>
"""


class BlockTradingStrategy(Strategy):

    def __init__(self, trade):
        self.trade = trade

    def handle_strategy(self):
        if self.trade.amount > 1000000:
            trade_time_s = self.trade.trade_time.strftime('%Y-%m-%d %H:%M:%S')
            subject = "股票:[%s]在%s有交易大单操作" % (self.trade.stock_code, trade_time_s)
            content = self.get_mail_content()
            Mail().send(subject, content, subtype='html')

    def get_mail_content(self):
        with TradeService() as trade_service:
            db_trades = trade_service.query_trades(self.trade.stock_code, 10)
            return Template(MAIL_CONTENT_TEMPLATE).render(db_trades=db_trades, trade=self.trade)