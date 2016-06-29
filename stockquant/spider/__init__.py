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
import requests
import requests.exceptions


class SpiderError(Exception):
    pass


class Spider(object):

    @classmethod
    def fetch(cls, method, url, **kwargs):
        try:
            r = requests.request(method, url, **kwargs)
            if r.status_code == 200:
                return r.json()
            else:
                raise SpiderError("request url:[%s] response code:[%s] message:[%s]" % (url, r.status_code, r.text))
        except requests.exceptions.RequestException, e:
            raise SpiderError("request url:[%s] error:[%s]" % (url, e.message))


