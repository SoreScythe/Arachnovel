from settings import task_limit
from core.tools import random_proxy, random_ua
from bs4 import BeautifulSoup as bs4
from aiohttp import ClientSession, client_exceptions
from os import path
import asyncio

class AsyncHandler:
    # def __init__(self):
    #     self.semaphore = asyncio.BoundedSemaphore(task_limit)
    async def async_soup(self, url, session):
        session.proxies['http'] = f'https://{random_proxy()}'
        # session.headers = headers
        headers = self.headers
        headers['User-Agent'] = random_ua()
        try:
            async with session.get(url, headers=headers) as resp:
                # print('Fetching', url)
                if not resp.status == 200:
                    return
                soup = await resp.text()
                soup = bs4(soup, "lxml")
                self.chapter_count += 1
                # print(f'Fetched {self.chapter_count} chapters')
                return soup
        except client_exceptions.ServerDisconnectedError:
            print('Disconnected on ip:', session.proxies['http'])
        except client_exceptions.ClientConnectorError:
            print('Cannot connect to host with ip:', session.proxies['http'])
        except client_exceptions.ClientPayloadError:
            print('Incomplete Payload with:', session.proxies['http'])
        except client_exceptions.ClientOSError:
            print('Connection reset on:', session.proxies['http'])
        except asyncio.exceptions.TimeoutError:
            print('Async time out')
    def async_do(self, index_urls, method):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.run_async(index_urls, method))
            loop.close()
        except KeyboardInterrupt:
            print('Stopped..')
            exit()
    
    async def run_async(self, chapters, method):
        jobs = []
        semaphore = asyncio.BoundedSemaphore(task_limit)
        counter = 1
        async with ClientSession() as session:
            for chapter in chapters:
                session.proxies = {'http': f'https://{random_proxy()}'}
                session.headers['User-Agent'] = random_ua()
                jobs.append(asyncio.create_task(self.async_job(chapter, method, session, semaphore)))
            try:
                await asyncio.gather(*jobs)
            except KeyboardInterrupt:
                print('Stopping..')

    async def async_job(self, chapter, method, session, sem):
        async with sem:
            try:
                chapnum = f"{int(chapter['chapter']):07}"
                fname = f"{self.cache_dir}/chapter_{chapnum}.json"
                if path.exists(fname):
                    print(f"Chapter {chapter['chapter']} already exists")
                    return
                soup = None
                while soup is None:
                    soup = await self.async_soup(chapter['url'], session)
                print('Fetched chapter', chapter['chapter'], chapter['title'])
                method(soup, fname, chapter['title'])
            except KeyboardInterrupt:
                print('Stopped')
                exit()
    async def __save_chapter(self, chap, session, sem):
        async with sem:
            print(f'Fetching chapter {chap["chapter"]} - {chap["title"]}')
            chapter = {}
            soup = await self.async_soup(chap['url'], session)
            chapter['chapter'] = f'{chap["chapter"]:07}'
            chapter['title'] = str(chap['title'])
            chapter['content'] = self.get_chapter_div(soup)
            print('chapter')
            # with open(f'{cache_directory}/chapter_{chapnum}.json', 'w') as chap_file:
            #     json.dump(chap, chap_file)
            #     chap_file.close()
    async def get_chapter_urls(self, url, session, sem):
        async with sem:
            soup = await self.async_soup(url, session)
            for row in  soup.find_all('ul', {'class' : 'list-chapter'}):
                for chap in row.find_all('a'):
                    title = chap['title'].text.strip()
                    # this is the stop
                    # bookmark
            
            count 
    async def __get_chap_urls(self, page_urls):
        jobs = []
        sempahore = asyncio.BoundedSemaphore(task_limit)
        async with ClientSession() as session:
            for url in page_urls:
                    jobs.append(asyncio.create_task(self.__get_chapter_urls(url, session, sem)))
            await asyncio.gather(*jobs)
        
    async def __fetch_chapters(self, chapter_list):
        jobs = []
        semaphore = asyncio.BoundedSemaphore(task_limit)
        async with ClientSession() as session:
            for chapter in chapter_list:
                    jobs.append(asyncio.create_task(self.__save_chapter(chapter, session, semaphore)))
            await asyncio.gather(*jobs)

    def fetch_chapters(self, url_list):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__fetch_chapters(url_list))
        loop.close()
