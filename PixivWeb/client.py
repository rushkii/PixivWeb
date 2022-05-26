from PixivWeb.scaffold import Scaffold
from PixivWeb.methods import Methods

from aiohttp import ClientSession
from bs4 import BeautifulSoup as bsoup
import json

class Client(Methods, Scaffold):
    def __init__(self, download_dir: str = None):
        self.download_dir = download_dir
    
    async def _request(self, url: str, **kwargs) -> bsoup:
        async with ClientSession() as ses:
            async with ses.get(url, **kwargs) as res:
                return bsoup(await res.text(), 'lxml')

    async def _ajax_request(self, url: str, **kwargs) -> bsoup:
        async with ClientSession() as ses:
            async with ses.get(url, **kwargs) as res:
                return json.loads(await res.text())

    async def _download_request(self, url: str, **kwargs) -> bsoup:
        kwargs['headers'] = {"Referer": "https://www.pixiv.net/"}
        async with ClientSession() as ses:
            async with ses.get(url, **kwargs) as res:
                return await res.read()