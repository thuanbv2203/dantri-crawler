# -*- coding: utf-8 -*-
import time
import urllib.request
from bs4 import BeautifulSoup
import random

def error_link_log(content):
  with open("link.log", "a") as log_file:
    log_file.write(content+ "\n")

class HtmlParser:
  def __init__(self):
    self.proxies = []
  @staticmethod
  def get_proxy():
    proxies = ['http://125.212.217.215:80', 'http://113.161.68.146:8080', 'http://118.69.180.35:3128']
    return proxies[random.randint(0, len(proxies) - 1)]

  @staticmethod
  def get_useragent():
    useragents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36','Mozilla/5.0', 'Opera/9.00 (Windows NT 5.1; U; en)', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)']
    return useragents[random.randint(0, len(useragents) - 1)]

  @staticmethod
  def get_html(url, loop = 1, error = False):
    if not error:
      print('Getting data from url: ' + url)
    response = ''
    try:
      req = urllib.request.Request(url)
      req.add_header('User-agent', HtmlParser.get_useragent())
      opener = urllib.request.urlopen(req, timeout = 100)
      response = opener.read().decode('utf-8')
    except Exception as e:
      print('[ERROR]' + str(e))
      print('Try again in 5 seconds.')
      time.sleep(5)
      response = False
      error_link_log(url)
    return response
