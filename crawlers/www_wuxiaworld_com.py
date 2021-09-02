from core.tools import random_proxy, random_ua
from core.handlers import AsyncHandler
from settings import cache_dir #, task_limit

from bs4 import BeautifulSoup as bs4
from requests import Session
from re import sub
import asyncio
import json

# static for this website
website = 'www.wuxiaworld.com'
headers = {
    'User-Agent': '',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Alt-Used': 'www.wuxiaworld.com',
    'Connection': 'keep-alive',
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
        self.headers = {} # headers not working!

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
        info_div = soup.find('div', {'class': 'section-content'})
        novel = {
            "title": self.get_title(info_div),
            'author': self.get_author(info_div),
            'synopsis': self.get_synopsis(soup)
        }
        # self.get_chapters(soup)
        self.cache_dir = f"{self.cache_dir}/{novel['title'].replace(' ', '_')}"
        return novel#, self.chapters
    
    def get_synopsis(self, soup):
        synopsis = soup.find_all('div', {'class': 'fr-view'})[1]
        return synopsis.text.strip()

    def get_author(self, info_div):
        return info_div.find_all('dd')[1].text.strip()

    def get_title(self, info_div):
        return info_div.find("h2").text.strip()

    def get_chapters(self, soup):
        div = soup.find('div', {"class": "tab-content novel-content"})
        chapterlist = [chapter.a for chapter in div.find_all('li', {'class': 'chapter-item'})]
        for item in chapterlist:
            chapter = ''.join([char for char in item['href'].strip() if char.isdigit()])
            title = sub('.*[-|:][ ]?', '', item.text.strip())
            self.chapters.append({'chapter':chapter, 'title':title, 'url':f"https://{website}{item['href']}"})
        return self.chapters
    def save_chapter(self, soup, chapter_fname, chaptitle):
        assert not soup is None, "Chapter soup is empty"
        try:
            chapter_div = soup.find('div', {'id':'chapter-content'})
        except AttributeError:
            print(soup)
        for tag in ['style', 'div', 'script', ['a', {'class': 'chapter-nav'}]]:
            for a in chapter_div.find_all(tag):
                try:
                    a.decompose()
                except TypeError:
                    pass
        for tag in chapter_div.find_all():
            tag.attrs = {}
        chapter_div.attrs = {}
        chap = {
            'title': chaptitle,
            "content": str(chapter_div)
        }
        with open(chapter_fname, 'w') as cf:
            json.dump(chap, cf)
            cf.close()
        # print(chapter_div)
        # print(F"Fetched chapter {chapnum} - {chaptitle}")
        # print(chapter_div)
        
