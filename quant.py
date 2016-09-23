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
import signal
from stockquant.spider.tencent import TencentRunner
from stockquant.strategy.blocktrading import BlockTradingStrategy


def do_quant(stock_code, interval=5):


    def tencent_runner_cb(trade):
        BlockTradingStrategy().handle_strategy(trade)

    runner = TencentRunner(stock_code, interval, tencent_runner_cb)

    def signal_handler(signum, frame):
        print 'Catch Crtl+C signal. System exit.'
        runner.stop()

    runner.setDaemon(True)
    runner.start()
    runner.join()


class QuantRunner(object):

    def __init__(self, stock_code, interval=5):
        self.stock_code = stock_code
        self.interval = interval
        self.tencent_runner = TencentRunner(stock_code, interval, self.tencent_runner_cb)

    def do_quant(self):
        if self.tencent_runner.isAlive():
            raise RuntimeError("TencentRunner is running")
        self.tencent_runner.setDaemon(True)
        self.tencent_runner.start()
        self.tencent_runner.join()

    @classmethod
    def tencent_runner_cb(cls, trade):
        BlockTradingStrategy().handle_strategy(trade)

    def signal_handler(self, signum, frame):
        print 'Catch Crtl+C signal. System exit.'
        self.tencent_runner.stop()


if __name__ == '__main__':
    quant_runner = QuantRunner('sh601989')
    signal.signal(signal.SIGINT, quant_runner.signal_handler)
    quant_runner.do_quant()