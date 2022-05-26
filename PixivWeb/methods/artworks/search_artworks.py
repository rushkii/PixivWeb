from PixivWeb.scaffold import Scaffold
from PixivWeb import types

from typing import Dict, List
import json, dateparser

class SearchArtworks(Scaffold):
    async def search_artworks(self, keyword: str) -> List["types.Artworks"]:
        res = await self._ajax_request(f"{self._PIXIV_AJAX_URL}/search/top/{keyword}")
        data = res.get('body')

        if res['error']:
            raise Exception(f'Error while searching for "{keyword}"')

        return data