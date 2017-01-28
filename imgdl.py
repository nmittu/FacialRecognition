import sys
from GoogleScraper import scrape_with_config, GoogleSearchError
from GoogleScraper.database import ScraperSearch, SERP, Link
import threading,requests, os, urllib

class FetchResource(threading.Thread):
    """Grabs a web resource and stores it in the target directory"""
    def __init__(self, target, urls):
        super().__init__()
        self.target = target
        self.urls = urls

    def run(self):
        for url in self.urls:
            url = urllib.parse.unquote(url)
            with open(os.path.join(self.target, url.split('/')[-1].split("?")[0]), 'wb') as f:
                try:
                    content = requests.get(url).content
                    f.write(content)
                except Exception as e:
                    pass
                print('[+] Fetched {}'.format(url))

keyword = sys.argv[1]
print(keyword)
target_dir = keyword+"/"

config = {
    'keyword': keyword, # :D hehe have fun my dear friends
    'search_engines': ['yandex', 'google', 'bing', 'yahoo'], # duckduckgo not supported
    'search_type': 'image',
    'scrapemethod': 'selenium'
}

try:
    search = scrape_with_config(config)
except GoogleSearchError as e:
    print(e)

image_urls = []

for serp in search.serps:
    image_urls.extend(
        [link.link for link in serp.links]
    )

print('[i] Going to scrape {num} images and saving them in "{dir}"'.format(
    num=len(image_urls),
    dir=target_dir
))

try:
    os.mkdir(target_dir)
except FileExistsError:
    pass

num_threads = 100

threads = [FetchResource(target_dir, []) for i in range(num_threads)]

while image_urls:
    for t in threads:
        try:
            t.urls.append(image_urls.pop())
        except IndexError as e:
            break

threads = [t for t in threads if t.urls]

for t in threads:
    t.start()

for t in threads:
    t.join()
