# -*- coding: utf-8 -*-

import requests
import re
from lxml import etree
from io import StringIO
import md5
import random
import urllib
import json


def translate(query_str):
    URL = "http://api.fanyi.baidu.com/api/trans/vip/translate"
    appid = '20151224000008220'
    secretKey = 'fLmNUjG9FY4JYHxW3WqW'

    q = query_str
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    URL = URL+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    r = requests.get(URL)
    result = r.text
    json_obj = json.loads(result)
    dst = json_obj["trans_result"][0]["dst"]
    return dst


if __name__ == "__main__":
    q_str = "Prediction Function Call Failed"
    translate(q_str)
