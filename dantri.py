# -*- coding: utf-8 -*-

import sqlite3
from HtmlParser import HtmlParser
from bs4 import BeautifulSoup
import re

class DanTri:
  def __init__(self, link, category):
    response = HtmlParser.get_html(link, loop = 5)
    self.setValid(True)
    if not response:
      self.setValid(False)
    else:
      self.soup = BeautifulSoup(response, 'html.parser')
      self.link = link.lstrip().rstrip()
      self.category = category
      self.page_id = self.get_pageid(link)
      self.title = self.get_title()
      self.brief = self.get_brief()
      self.content = self.get_content()
      self.time = self.get_time()
      self.author = self.get_author()
      self.tags = self.get_tags()
  
  def setValid(self, flag):
    self.isValid = flag

  def getValid(self):
    return self.isValid

  def get_pageid(self,link):
    pageid = re.findall('\d+', link)[-1] 
    if pageid:
      return pageid
    else:
      return ''

  def get_title(self):
    title = self.soup.find('h1', attrs={'class':'fon31'})
    if title:
      return title.string.strip()
    else:
      return ''

  def get_brief(self):
    brief = self.soup.find('h2', attrs={'class':'fon33'})
    if brief:
      return brief.get_text().replace('Dân trí ','').strip()
    else:
      return ''

  def get_content(self):
    content_div = self.soup.find('div', attrs={'id':'divNewsContent'})
    if content_div:
      content = ''
      for con in content_div.find_all('p', attrs={'style':''}):
        content += '\n' + con.get_text()
      return self.get_brief() + content.strip()
    else:
      return self.get_brief()

  def get_time(self):
    time = self.soup.find('span', attrs={'class':'tt-capitalize'})
    if time:
      return time.get_text().strip()
    else:
      return ''


  def get_author(self):
    content_div = self.soup.find('div', attrs={'id':'divNewsContent'})
    author_right = content_div.find('p', attrs={'style':'text-align: right;'})
    author_left = content_div.find('p', attrs={'style':'text-align: left;'})
    if author_right:
      return author_right.get_text().strip()
    if author_left:
      return author_left.get_text().strip()
    return ''

  def get_tags(self):
    content_div = self.soup.find('div', attrs={'id':'divNewsContent'})
    tags_item = content_div.find('span', attrs = {'class':'news-tags-item'})
    if tags_item:
      return tags_item.get_text().strip()
    else:
      return ''