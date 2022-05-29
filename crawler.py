import requests
import os
from tinydb import TinyDB
from html.parser import HTMLParser


db = TinyDB("results.json")

def get_host(url):
    while os.path.dirname(url) not in ["http:", "https:"]:
        url = os.path.dirname(url)

    return url

class Parser(HTMLParser):
    def __init__(self):
        super(Parser, self).__init__(convert_charrefs=True)
        self.url = ""
        self.urls = []
        self.meta_description = ""
        self.title = ""
        self.paragraph_content = ""
        self.paragraph = False
        self.set_description = False
        self.set_title = False
    

    def set_url(self, url):
        if url[-1] == "/":
            if os.path.dirname(url[:-1]) not in ["http:", "https:"]:
                url = url[:-1]
        self.url = url

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            for attr in attrs:
                if attr[0] == "name" and attr[1] == "description":
                    self.set_description = True
                
                if self.set_description:
                    if attr[0] == "content":
                        self.meta_description = attr[1]
                        self.set_description = False

        elif tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    link = attr[1]

                    if link:
                        if link[0] == "/":
                            link = get_host(self.url) + link
                            self.urls.append(link)
                        elif "http://" in link and link.index("http://") == 0:
                            self.urls.append(link)
                        elif "https://" in link and link.index("https://") == 0:
                            self.urls.append(link)

        elif tag == "p" and len(self.paragraph_content) < 100:
            self.paragraph = True

        elif tag == "title":
            self.set_title = True

    def handle_endtag(self, tag):
        if tag == "p":
            self.paragraph = False

    def handle_data(self, data):
        if self.set_title:
            self.title = data
            self.set_title = False
        elif self.paragraph:
            self.paragraph_content += data

    def clear(self):
        self.urls = []
        self.meta_description = ""
        self.title = ""
        self.paragraph_content = ""
        self.paragraph = False
        self.set_description = False
        self.set_title = False


def crawl(start_queue):
    parser = Parser()

    queue = start_queue
    seen_urls = []
    while len(queue) > 0:
        if queue[0] not in seen_urls:
            try:
                print (queue[0])
                
                page = requests.get(queue[0])
                parser.set_url(queue[0])
                parser.feed(page.text)
                

                db.insert({
                    "title": parser.title,
                    "description": parser.meta_description,
                    "content": parser.paragraph_content,
                    "url": queue[0]
                })

                seen_urls.append(queue[0])
                queue = queue + parser.urls
                parser.clear()
            except Exception as e:
                print (e)

        queue = queue[1:]


crawl(["https://en.wikipedia.org/wiki/Music", "https://en.wikipedia.org/wiki/Cricket", "https://en.wikipedia.org/wiki/Football"])