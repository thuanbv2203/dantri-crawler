class DanTri:
  def __init__(self, link, category):
    response = get_html(link, loop = 5)
    if not response:
      return False
    self.soup = BeautifulSoup(response, 'html.parser')
    self.link = link.lstrip().rstrip()
    self.category = category
    self.page_id = get_pageid(link)
    self.title = get_title()
    self.brief = get_brief()
    self.content = get_content()
    self.time = get_time()
    self.author = get_author()
    self.tags = get_tags()

  def get_pageid(link):
    return re.findall('\d+', link)[-1]

  def get_title():
    title = self.soup.find('h1', attrs={'class':'fon31'})
    if title:
      return title.string
    else:
      return ''

  def get_brief():
    brief = self.soup.find('h2', attrs={'class':'fon33'})
    if brief:
      return brief.get_text().replace('Dân trí ','').strip()
    else:
      return ''

  def get_content():
    content_div = self.soup.find('div', attrs={'id':'divNewsContent'})
    if content_div:
      content = ''
      for con in content_div.find_all('p', attrs={'style':''}):
        content += '\n' + con.get_text()
      return get_brief() + content.strip()
    else:
      return get_brief()

  def get_time():
    time = self.soup.find('span', attrs={'class':'tt-capitalize'})
    if time:
      return time.get_text().strip()
    else:
      return ''


  def get_author():
    content_div = self.soup.find('div', attrs={'id':'divNewsContent'})
    author_right = content_div.find('p', attrs={'style':'text-align: right;'})
    author_left = content_div.find('p', attrs={'style':'text-align: left;'})
    if author_right:
      return author_right.get_text().strip()
    if author_left:
      return author_left.get_text().strip()
    return ''

  def get_tags():
    tags_item = content_div.find('span', attrs = {'class':'news-tags-item'})
    if tags_item:
      return tags_item.get_text().strip()
    else:
      return ''
