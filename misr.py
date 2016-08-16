# -*- coding: utf-8 -*-
import sqlite3
import urllib.request
import zlib
from bs4 import BeautifulSoup
import re
import random
from dantri import DanTri


def random_proxy():
  PROXIES = ['123.30.238.16:3128', '113.161.4.250:8080', '113.161.68.146:8080']
  return PROXIES[random.randint(0, len(PROXIES) - 1)]

def print_error():
  print('error')

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

def get_content(url, page = 1, dbName = 'database.db', category=''):
  counter = page
  while True:
    print('page: ' + str(counter) + '----------------------------------------------')
    dantris = []
    category_link = url + '/' + category + '/trang-' + str(counter) + '.htm'
    print(category_link)
    response = get_html(category_link, loop = 5)
    if not response:
      print('continue with another page')
      continue
    if not check_content(response):
      print('break in check content')
      break
    for index, link in enumerate(get_link_in_page(response)):
      dantri = DanTri(link, category)
      if not dantri:
        continue
      # print('[' + str(index + 1) + ']' + dantri.title + ' - ' + dantri.time)
      # dantris.append(DanTri(link, category))
    # insert_data(dantris, dbName)
    counter += 1

def get_link_in_page(response):
  links = []
  soup = BeautifulSoup(response, 'html.parser')
  hrefs = soup.find_all('a', attrs = {'class':'fon6'})
  for href in hrefs:
    links.append('http://dantri.com.vn' + href['href'])
  return links


def check_content(response):
  soup = BeautifulSoup(response, 'html.parser')
  links = soup.find_all('a', attrs = {'class':'fon6'})
  return len(links) > 0

def insert_data(datas, dbName):
  conn = sqlite3.connect(dbName)
  cur = conn.cursor()
  cur.execute('''CREATE TABLE IF NOT EXISTS DATA (
    id INTEGER PRIMARY KEY, 
    page_id TEXT, 
    title TEXT, 
    category TEXT, 
    brief TEXT, 
    content TEXT, 
    time TEXT, 
    link TEXT, 
    author TEXT,
    tags TEXT
    );''')
  for data in datas:
    cur.execute("INSERT INTO DATA VALUES (NULL,'"+ data.page_id +"','"+ data.title +"','"+ data.category +"','"+ data.brief +"','"+ data.content +"','"+ data.time +"','"+ data.link +"','"+ data.author +"','"+ data.tags +"')")
  conn.commit()
  conn.close()

TOPIC = ['su-kien', 'xa-hoi', 'the-gioi', 'the-thao', 'giao-duc-khuyen-hoc', 'tam-long-nhan-ai', 'kinh-doanh', 'van-hoa', 'giai-tri', 'phap-luat', 'nhip-song-tre', 'suc-khoe', 'suc-manh-so', 'o-to-xe-may', 'tinh-yeu-gioi-tinh', 'chuyen-la']
URL = 'http://dantri.com.vn/'

# createDatabase('database1.db')
get_content('http://dantri.com.vn', category = 'phap-luat')
# print(check_link('http://dantri.com.vn/phap-luat/trang-6000.htm'))
# print(random_proxy())