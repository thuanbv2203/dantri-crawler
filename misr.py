# -*- coding: utf-8 -*-
import sqlite3
import urllib.request
import zlib
from bs4 import BeautifulSoup
import re
import random
from dantri import DanTri
from HtmlParser import HtmlParser
def get_content(url, page = 1, dbName = 'database.db', category=''):
  counter = page
  while True:
    print('page: ' + str(counter) + '----------------------------------------------')
    dantris = []
    category_link = url + '/' + category + '/trang-' + str(counter) + '.htm'
    print(category_link)
    response = HtmlParser.get_html(category_link, loop = 5)
    if not response:
      print('continue with another page')
      continue
    if not check_content(response):
      print('break in check content')
      break
    for index, link in enumerate(get_link_in_page(response)):
      dantri = DanTri(link, category)
      if not dantri.getValid():
        continue
      dantris.append(dantri)
    insert_data(dantris, dbName)
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
  try:
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
  except Exception as e:
    print('error in database pharse')

TOPIC = ['su-kien', 'xa-hoi', 'the-gioi', 'the-thao', 'giao-duc-khuyen-hoc', 'tam-long-nhan-ai', 'kinh-doanh', 'van-hoa', 'giai-tri', 'phap-luat', 'nhip-song-tre', 'suc-khoe', 'suc-manh-so', 'o-to-xe-may', 'tinh-yeu-gioi-tinh', 'chuyen-la']
URL = 'http://dantri.com.vn/'

# createDatabase('database1.db')
get_content('http://dantri.com.vn', category = 'phap-luat')
# print(check_link('http://dantri.com.vn/phap-luat/trang-6000.htm'))
# print(random_proxy())
# print(HtmlParser.get_html(' http://dantri.com.vn/phap-luat/ngao-da-nguoi-dan-ong-cam-tuyp-nuoc-nhua-doa-ban-cong-an-201608060809306.htm'))