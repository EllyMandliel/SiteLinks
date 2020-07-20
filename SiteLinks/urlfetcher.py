import aiohttp
import asyncio
import re
import urllib.parse as parser
from bs4 import BeautifulSoup
from functools import partial
import argparse

DEFAULT_DEPTH = 3


async def validate_link(link, allow_outside=False):
    if not link:
        return
    if re.compile('[^/]*:').match(link):
        return
    if re.compile('^https?://').match(link):
        if allow_outside:
            return link
    else:
        return re.sub('#.*', '', link)


class URLFetcher:

    def __init__(self, start_url, depth, allow_outside=False, validate_status=False):
        self.depth = depth
        self.allow_outside = allow_outside
        self.validate_status = validate_status
        if self.validate_status:
            self.link_status = {}
        self.links = []
        self.start_url = start_url
        parsed_url = parser.urlparse(self.start_url)
        host = parsed_url.netloc.replace(':80', '')
        self.basepath = f'{parsed_url.scheme}://{host}'

    async def read_links(self, req):
        text_content = await req.text()
        soup = BeautifulSoup(text_content, 'html.parser')
        links = map(lambda x: x.get('href'), soup.findAll('a'))
        return await asyncio.gather(*map(partial(validate_link, allow_outside=self.allow_outside), links))

    def join_link(self, path):
        return parser.urljoin(self.basepath, path)

    async def add_links(self, links):
        joined = filter(lambda x: x not in self.links, map(self.join_link, links))
        new_values = set(joined)
        self.links.extend(new_values)
        return new_values

    async def run(self):
        await self.connect(self.start_url, self.depth)

    async def request_url(self, url):
        async with aiohttp.request('GET', url) as r:
            links = await self.read_links(r)
            status = r.status
        return links, status

    async def connect(self, url, depth):

        if depth == 0 and not self.validate_status:
            return

        links, status = await self.request_url(url)

        if self.validate_status:
            self.link_status[url] = status
            if depth == 0:
                return

        await asyncio.gather(*[self.connect(i, depth - 1) for i in await self.add_links(links)])



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='Hostname to scan')
    parser.add_argument('-s', help='Resolve the status for each URL', action="store_true")
    parser.add_argument('-o', help='Include urls not at the host', action="store_true")
    parser.add_argument('--depth', help='Depth of search. Default: 3', default=3)
    return parser.parse_args()


async def main():
    args = parse_args()
    fetcher = URLFetcher(args.host, allow_outside=args.o, validate_status=args.s,
                         depth=int(args.depth))

    await fetcher.run()
    if args.s:
        print("\n".join([f'{value}: {key}' for key, value in fetcher.link_status.items()]))
    else:
        print("\n".join(fetcher.links))
