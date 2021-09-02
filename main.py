#!/usr/bin/env python3
from argparse import ArgumentParser
<<<<<<< HEAD
from prompt_toolkit import prompt
from ebooklib import epub

from os import getcwd, path, mkdir, listdir
from sys import argv
from importlib import import_module
from urllib.parse import urlparse, urlunparse
from types import SimpleNamespace
from time import sleep
import shutil
import json
import re

# cache_directory = path.join(path.abspath(environ["HOME"]), 'NovelCache')
cache_directory = f'{path.abspath(getcwd())}/.novelcache'

class EbookCompiler(epub.EpubBook):
    def __init__(self, novel):
        epub.EpubBook.__init__(self)
        self.set_title(novel.title)
        self.set_language("en")
        self.add_author(novel.author)
        self.add_metadata("DC", "description", novel.synopsis)
    def compile(self, cache_dir=cache_directory):
        flist = sorted([f'{cache_dir}/{chap}' for chap in listdir(cache_dir) if chap.startswith('chapter')])
        self.spine = ['nav']
        # self.chap_start = 0
        # count = 0
        if len(flist) < 1:
            print('No chapter to compile')
            exit()
        print('Compiling downloaded chapters')
        for file in flist:
            chapter = json.load(open(file, 'r'))
            chap = epub.EpubHtml(title=f"Chapter {chapter['chapter']} - {chapter['title'].strip()}", file_name=f'chap_{int(chapter["chapter"]):07}.xhtml', lang='hr')
            chap.content= chapter['content'].encode('utf-8')
            self.add_item(chap)
            self.toc.append(chap)
            self.spine.append(chap)
            # if self.chap_start == 0:
                # self.chap_start = chapter['chapter']
            # count += 1
    def save(self, output):
        self.add_item(epub.EpubNcx())
        self.add_item(epub.EpubNav())
        style = 'p { text-align : left; }'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.add_item(nav_css)
        epub.write_epub(output, self, {})
        
class Parser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self, prog='novelcrawl')
        download = self.add_mutually_exclusive_group(required=True)
        download.add_argument('-u', '--url', help='novel url', type=str)
        download.add_argument('-q', '--query', help='query string', type=str)
        # self.add_argument('-up', '--update-cache', help='ignore existing cache', default=True, action='store_false')
        self.add_argument('-cl', '--clean-cache', help='delete novel cache after compiling', default=False, action='store_true')
    def compile(self, arguments):
        arguments = self.parse_args(arguments)
        params = SimpleNamespace(
            clean_cache = arguments.clean_cache
        )
        if arguments.query is None:
            params.operation = 'download'
            params.url = urlparse(arguments.url)
            if params.url.scheme == "" or params.url.path == '':
                print(f'Invalid url: {arguments.url}')
                exit()
        elif arguments.url is None:
            params.operation = 'query'
            params.query = arguments.query
        return params

def import_crawler(website):
    "Import crawler based on websites netloc or domain name"
    crawler = re.sub('\.|-', '_', website)
    crawler = f"crawlers.{crawler}"
    try:
        crawler = import_module(crawler)
    except ImportError:
        print(f"Cannot import: {crawler}")
        print("Site is currently not supported")
        exit()
    return crawler
    
def download_novel(crawler, urlObj):
    "To seperate the download from the search function"
    novel = crawler.getInformation(urlunparse(urlObj))
    global cache_directory
    site = re.sub("-| |\.", "_", urlObj.netloc)
    cache_directory = f'{cache_directory}/{site}/{novel.info.title.replace(" ", "_")}'
    print(f'Title: {novel.info.title}')
    sleep(0.5)
    print(f'Author: {novel.info.author}')
    sleep(0.5)
    print(f'Synopsis: {novel.info.synopsis}')
    sleep(0.5)
    print(f'Chapters: {len(novel.chapters) - 1}')
    create_cache_dir(cache_directory)
    output = f'{path.abspath(getcwd())}/{novel.info.author} - {novel.info.title}.epub'
    # exit(0)
    try:
        crawler.download_chapters(novel.chapters, cache_directory)
        # book = EbookCompiler(novel.info)
        # book.compile()
        # book.save(output)
    except KeyboardInterrupt:
        pass
    finally:
        book = EbookCompiler(novel.info)
        book.compile(cache_directory)
        book.save(output)
        print(f'Book saved to: {output}')
        delete_cache_dir(cache_directory)
def create_cache_dir(cd=cache_directory):
=======
from core.compiler import Compiler as compiler

from sys import argv
from urllib.parse import urlparse
from importlib import import_module
from os import path, mkdir
from time import sleep
# from settings import cache_dir

class Parser(ArgumentParser):
    def __init__(self):
        ArgumentParser.__init__(self)
        operation = self.add_mutually_exclusive_group(required=True)
        operation.add_argument('--url', '-u', help='Novel url', type=str)
        operation.add_argument('--query', '-q', help='Search query', type=str)
        self.add_argument('--verbose', '-v', required=False, default=False, action='store_true')
    def parse(self, arguments):
        arguments = self.parse_args(arguments)
        return arguments

def import_crawler(website):
    crawler = website.replace('.', '_')
    crawler = crawler.replace('-', '_')
    # crawler = import_module(f'crawlers.{crawler}')
    try:
        crawler = import_module(f'crawlers.{crawler}')
    except ImportError:
        print("Site is currently unsupported:", crawler)
        exit()
    return crawler.Crawler()

def download_novel(crawler, url):
    # try to import crawler for website
    novel = crawler.get_novel_details(url)
    cache_directory = crawler.cache_dir
    output = f"{novel['title'].replace(' ', '_')}.epub"
    print('Title:', novel['title'])
    print('Author:', novel['author'])
    print('Synopsis:', novel['synopsis'])
    print('Parsing chapter list...')
    sleep(1.5)
    chapters = crawler.get_chapters(crawler.soup)
    # print(chapters)
    # crawler.fetch_chapters(chapters[1:10])
    # print(chapters[1])
    create_cache_directory(cache_directory)
    crawler.async_do(chapters, crawler.save_chapter)
    print('Creating book skeleton...')
    book = compiler(novel)
    print('Compiling chapters...')
    book.compile_book(cache_directory)
    print('Saving ebook to:', output)
    book.save(output)
    
def create_cache_directory(cd):
>>>>>>> master
    directory = '/'
    for p in cd.split('/'):
        directory = path.join(directory, p)
        try:
            mkdir(directory)
<<<<<<< HEAD
            # print(f'created {directory}')
        except:
            pass

def delete_cache_dir(cd=cache_directory):
    print('Deleting cache directory...')
    try:
        shutil.rmtree(cd)
    except:
        pass

def query_novel(query_string):
    "Search novel string from available sites"
    print(f'Searching for novel/s: {query_string}')
    
if __name__ == "__main__":
    parser = Parser()
    arguments = parser.compile(argv[1:])
    
    if arguments.operation == 'download':
        crawler = import_crawler(arguments.url.netloc)
        download_novel(crawler, arguments.url)
    elif arguments.operation == 'query':
        query_novel(arguments.query)
=======
        except:
            pass

def main(args):
    if args.query is None:
        novel_url = urlparse(args.url)
        # validate the url
        if novel_url.scheme == '' or novel_url.path == '/':
            print("Invalid url given:", url)
            exit()
        # start downloading
        crawler = import_crawler(novel_url.netloc)
        download_novel(crawler, args.url)
    else:
        query_novel(args.query)

if __name__ == "__main__":
    parser = Parser()
    arguments = parser.parse(argv[1:])
    
    main(arguments)
        
>>>>>>> master
