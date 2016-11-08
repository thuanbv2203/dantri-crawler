# -*- coding: utf-8 -*-

import sqlite3
import urllib.request
import zlib
from bs4 import BeautifulSoup
import re
import random
from dantri import DanTri
from HtmlParser import HtmlParser


def write_log(content):
  with open("misr.log", "a") as log_file:
    log_file.write(content+ "\n")

def get_content(url, page = 1, dbName = 'database.db', category=''):
  counter = page
  while True:
    print('page: ' + str(counter) + '----------------------------------------------')
    dantri_list = []
    category_link = url + '/' + category + '/trang-' + str(counter) + '.htm'
    print(category_link)
    response = HtmlParser.get_html(category_link, loop = 5)
    if not response:
      print('continue with another page')
      continue
    if not check_content(response):
      write_log('Interrupt in category = ' + category + ', page = ' + str(page) + ', link = ' + category_link)
      break
    for index, link in enumerate(get_link_in_page(response)):
      dantri = DanTri(link, category)
      if not dantri.getValid():
        continue
      dantri_list.append(dantri)
    insert_data(dantri_list, dbName)
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
      cur.execute("INSERT INTO DATA VALUES (NULL,?,?,?,?,?,?,?,?,?)", (str(data.page_id),str(data.title),str(data.category),str(data.brief),str(data.content),str(data.time),str(data.link),str(data.author),str(data.tags)))
    conn.commit()
    conn.close()
  except Exception as e:
    print('error in database pharse')

TOPIC = ['su-kien', 'xa-hoi', 'the-gioi', 'the-thao', 'giao-duc-khuyen-hoc', 'tam-long-nhan-ai', 'kinh-doanh', 'van-hoa', 'giai-tri', 'phap-luat', 'nhip-song-tre', 'suc-khoe', 'suc-manh-so', 'o-to-xe-may', 'tinh-yeu-gioi-tinh', 'chuyen-la']
URL = 'http://dantri.com.vn/'

# createDatabase('database1.db')
for category in TOPIC:
  get_content(url = 'http://dantri.com.vn', page = 1, dbName = 'database.db', category=category)
