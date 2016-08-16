# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
class HtmlParser:
  def __init__(self):
    self.PROXIES = []


  def get_html(url, loop, error = False):
    if not error:
      print('Getting data from url: ' + url)
    value = ''
    try:
      proxy = random_proxy()
      proxy_handler = urllib.request.ProxyHandler({'http': random_proxy()})
      opener = urllib.request.build_opener(proxy_handler)
      req = opener.open(url)
      r = req.read()
      value = r.decode('utf-8')
    except Exception as e:
      print('Try again with another proxy.')
      if loop == 0:
        value = False
      else:
        value = get_html(url, loop - 1, True)
    return value
