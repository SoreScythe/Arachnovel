from ebooklib import epub
from os import listdir
import json

class Compiler(epub.EpubBook):
    def __init__(self, novel):
        epub.EpubBook.__init__(self)
        self.set_title(novel["title"])
        self.set_language('en')
        self.add_author(novel['author'])
        self.add_metadata("DC", 'description', novel['synopsis'])
    def compile_book(self, path):
        flist = sorted([f'{path}/{chap}' for chap in listdir(path) if chap.startswith('chapter')])
        self.spine = ['nav']
        if len(flist) < 1:
                print('No chapter to compile')
                exit()
        print('Compiling downloaded chapters')
        counter = 0
        for file in flist:
                counter += 1
                chapter = json.loads(open(file, 'r').read())
                chap = epub.EpubHtml(title=f"Chapter {counter} - {chapter['title'].strip()}", file_name=f'chap_{counter:07}.xhtml', lang='hr')
                chap.content= chapter['content'].encode('utf-8')
                self.add_item(chap)
                self.toc.append(chap)
                self.spine.append(chap)
        
    def save(self, output):
        self.add_item(epub.EpubNcx())
        self.add_item(epub.EpubNav())
        style = 'p { text-align : left; }'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.add_item(nav_css)
        epub.write_epub(output, self, {})