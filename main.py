#!/usr/bin/env python3
from argparse import ArgumentParser
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
    directory = '/'
    for p in cd.split('/'):
        directory = path.join(directory, p)
        try:
            mkdir(directory)
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
        
