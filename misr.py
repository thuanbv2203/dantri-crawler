# -*- coding: utf-8 -*-
import sqlite3
import urllib.request
import zlib
from bs4 import BeautifulSoup
import re
class DanTri:
  def __init__(self, link, category):
    response = get_html(link)
    soup = BeautifulSoup(response, 'html.parser')
    title = soup.find('h1', attrs={'class':'fon31'}).string
    brief = soup.find('h2', attrs={'class':'fon33'}).get_text().replace('Dân trí ','')
    content_div = soup.find('div', attrs={'id':'divNewsContent'})
    content = ''
    for con in content_div.find_all('p', attrs={'style':''}):
      content += '\n'+con.get_text()
    time = soup.find('span', attrs={'class':'tt-capitalize'}).get_text()
    tags = ''
    tags_item = content_div.find('span', attrs = {'class':'news-tags-item'})
    if(tags_item):
      tags = tags_item.get_text()
    author = content_div.find('p', attrs={'style':'text-align: right;'}).get_text()
    page_id =  re.findall('\d+', link)[-1]

    self.page_id = page_id.lstrip().rstrip()
    self.category = category.lstrip().rstrip()
    self.title = title.lstrip().rstrip()
    self.brief = brief.lstrip().rstrip()
    self.content = brief.lstrip().rstrip() + content.lstrip().rstrip()
    self.time = time.lstrip().rstrip()
    self.author = author.lstrip().rstrip()
    self.link = link.lstrip().rstrip()
    self.tags = tags.lstrip().rstrip()

def print_error():
  print('error')

def get_html(url):
  value = ''
  try:
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req)
    value = r.read().decode('utf-8')
  except ValueError:
    # print(ValueError)
    value = False
  return value

def get_content(url, page = 6, dbName = 'database.db', category=''):
  counter = page
  while True:
    print('page: ' + str(counter) + '----------------------------------------------')
    dantris = []
    parent_link = url + '/' + category + '/trang-' + str(counter) + '.htm'
    if not check_link(parent_link):
      break
    # link = get_link_in_page(parent_link)[0]
    for index, link in enumerate(get_link_in_page(parent_link)):
      dantri = DanTri(link, category)
      print('[' + str(index + 1) + ']' + dantri.title + ' - ' + dantri.time)
      dantris.append(DanTri(link, category))
    insert_data(dantris, dbName)
    counter += 1

def get_link_in_page(url):
  links = []
  response = get_html(url)
  soup = BeautifulSoup(response, 'html.parser')
  hrefs = soup.find_all('a', attrs = {'class':'fon6'})
  for href in hrefs:
    links.append('http://dantri.com.vn' + href['href'])
  return links

def check_link(url):
  response = get_html(url)
  if (response == False):
    return False
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