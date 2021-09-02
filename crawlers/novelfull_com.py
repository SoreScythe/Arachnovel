from core.tools import random_proxy, random_ua
from core.handlers import AsyncHandler
from settings import cache_dir

from re import sub
from requests import Session
from types import SimpleNamespace
from bs4 import BeautifulSoup as bs4

# static for this website
website = 'novelfull.com'
headers = {
    'User-Agent': None,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

class Crawler(AsyncHandler):
    def __init__(self):
        self.cache_dir = cache_dir + "/" + sub('\.|-', '_', website)
        self.title = ''
        self.author = ''
        self.synopsis = ''
        self.chapters = {}
        self.chapter_count = 0

    def get_soup(self, url):
        with Session() as session:
            session.proxies = {'http': f'https://{random_proxy()}'}
            session.headers = headers
            session.headers['User-Agent'] = random_ua()
            soup = session.get(url)
            soup = bs4(soup.content, 'lxml')
            return soup
    
    def get_novel_details(self, url):
        soup = self.get_soup(url)
        info_div = soup.find('div', {'class': 'info'})
        novel = {
            "title": self.get_title(soup),
            "author": self.get_author(info_div),
            "synopsis": self.get_synopsis(soup)
        }
        self.cache_dir = self.cache_dir + f'/{novel["title"].replace(" ", "_")}'
        print("Title:", novel['title'])
        print("Author:", novel['author'])
        print("Synopsis:", novel['synopsis'])
        print('Fetching chapter urls...')
        chapter_indexes = self.get_index_page_urls(soup)
        chapters = self.async_do(chapter_indexes, self.get_chapter_urls_from_index)
        print(self.chapters.keys())
        exit()
        # chapters = self.chapter_list(soup)
        return novel, chapters

    def get_title(self, soup):
        title = soup.find('h3', {'class': "title"}).text.strip()
        return title

    def get_author(self, info_div):
        author = []
        for item in info_div.find_all('a')[0:1]:
            if item['href'].startswith('/author'):
                author.append(item.text.strip())
        author = ' '.join(author)
        return author

    def get_synopsis(self, soup):
        return soup.find('div', {'class':"desc-text"}).text.replace('  ', ' ')

    def get_chapter_div(self, soup):
        try:
            div = soup.find('div', {'id':'chapter-content'})
        except TypeError:
            print(soup)
            exit()
        for tag in ['script', 'div']:
            try:
                for t in div.find_all(tag):
                    t.decompose()
            except AttributeError:
                print(soup)
                exit()
        for nav in div.find_all('a', {'class': 'chapter-nav'}):
            nav.decompose()
        div.attrs = {}
        return str(div)
    def get_index_page_urls(self, soup):
        div = soup.find('ul', {'class' : 'pagination pagination-sm'})
        count, index_pages = 0, []
        last_page = div.find_all('a')[-1]['href']
        path = sub('[0-9]+$', '', last_page)
        pages = int(sub('.*page=', '', last_page)) + 1
        for page in range(1, pages):
            url = f'https://{website}{path}{page}'
            index_pages.append(url)
        return index_pages
    def get_chapter_urls_from_index(self, soup):
        for row in soup.find_all('ul', {'class': "list-chapter"}):
            for chap in row.find_all('a'):
                self.chapter_count += 1
                title = chap['title'].strip()
                title = sub('.*[–|-|:|-][ ]?', "", title)
                url = f'https://{website}{chap["href"]}'
                self.chapters[self.chapter_count] = [title, url]
