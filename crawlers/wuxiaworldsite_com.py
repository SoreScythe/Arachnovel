from core.tools import random_proxy, random_ua
from core.handlers import AsyncHandler
from settings import cache_dir #, task_limit

from bs4 import BeautifulSoup as bs4
from requests import Session
from re import sub
import asyncio
import json

website = 'wuxiaworldsite.com'
headers = {
    'Host': 'wuxiaworldsite.com',
    'User-Agent': '',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}
class Crawler(AsyncHandler):
    def __init__(self):
        # self.semaphore = asyncio.BoundedSemaphore(task_limit)
        self.cache_dir = f"{cache_dir}/{website.replace('.', '_')}"
        self.title = ''
        self.author = ''
        self.synopsis = ''
        self.chapters = []
        self.chapter_count = 0
        self.session = Session()
        self.headers = headers

    def get_soup(self, url):
        # with Session() as session:
        session = self.session
        session.proxies['http'] = f'https://{random_proxy()}'
        # session.headers = headers
        session.headers = self.headers
        session.headers['User-Agent'] = random_ua()
        soup = session.get(url)
        soup = bs4(soup.content, 'lxml')
        return soup
    def get_novel_details(self, url):
        soup = self.get_soup(url)
        self.soup = soup
        # self.title = 
        # self.author = 
        # self.synopsis = 
        novel = {
            "title": self.get_title(soup),
            'author': self.get_author(soup),
            'synopsis': self.get_synopsis(soup)
        }
        # self.get_chapters(soup)
        self.cache_dir = f"{self.cache_dir}/{novel['title'].replace(' ', '_')}"
        return novel#, self.chapters
    
    def get_synopsis(self, soup):
        descr = soup.find('div', {'class': "summary__content show-more"})
        for item in descr.find_all('p'):
            if item.strong:
                item.decompose()
        return descr.text.strip()
    def get_author(self, soup):
        author = soup.find('div', {'class':"author-content"}).a.text.strip()
        return author
    def get_title(self, soup):
        title = soup.find('title').text.strip()
        title = sub(' - .*', '', title)
        return title
    def get_chapters(self, soup):
        chapterlist = [item.a for item in soup.find_all('li', {'class': 'wp-manga-chapter'})]
        chapterlist.reverse()
        for item in chapterlist:
            # item = item.a
            chapter = ''.join([char for char in item['href'].strip() if char.isdigit()])
            title = sub('.*-[ ]?', '', item.text.strip())
            # self.chapters[chapter] = [title, item['href']]
            self.chapters.append({'chapter':chapter, 'title':title, 'url':item['href']})
        # keys = list(self.chapters.keys())
        # keys.reverse()
        # self.chapters = {int(k):self.chapters[k] for k in keys}
        return self.chapters
    def save_chapter(self, soup, chapter_fname, chaptitle):
        if soup == True:
            return
        try:
            chapter_div = soup.find('div', {'class':"text-left"})
        except AttributeError:
            print(soup)
        for tag in ['style', 'div', 'script', ]:
            for a in chapter_div.find_all(tag):
                try:
                    a.decompose()
                except TypeError:
                    pass
        chapter_div.attrs = {}
        chap = {
            'title': chaptitle,
            "content": str(chapter_div)
        }
        # chapnum = f"{int(chapter['chapter']:07}"
        # cfname = f"{self.cache_dir}/chapter_{chapnum}.json"
        with open(chapter_fname, 'w') as cf:
            json.dump(chap, cf)
            cf.close()
        # print(chapter_div)
        # print(F"Fetched chapter {chapnum} - {chaptitle}")
        # print(chapter_div)
        
