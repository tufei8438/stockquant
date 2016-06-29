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
import requests

from stockquant.utils.log import logger


class Holiday(object):

    _holiday_api_url = 'http://apis.baidu.com/xiaogg/holiday/holiday'
    _holiday_api_key = 'ca8597ff4906fd1fa7ccc1545438473f'

    _holidays = None

    @classmethod
    def get_holidays_by_api(cls):
        today = datetime.datetime.now()
        params = {'d': today.year}
        headers = {'apikey': cls._holiday_api_key}

        try:
            r = requests.get(cls._holiday_api_url, params=params, headers=headers)
            if r.status_code == 200:
                holidays = r.json()
                return holidays.get(str(today.year))
            else:
                return []
        except Exception:
            logger.exception("获取节假日接口异常")
            return []

    @classmethod
    def get_holidays(cls):
        if cls._holidays is None:
            cls._holidays = cls.get_holidays_by_api()
        return cls._holidays

    @classmethod
    def is_holiday(cls, date):
        if not isinstance(date, datetime.datetime):
            return False
        date_s = date.strftime('%m%d')
        return date_s in cls.get_holidays()