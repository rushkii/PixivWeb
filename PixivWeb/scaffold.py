from bs4 import BeautifulSoup

class Scaffold:
    _PIXIV_URL      = "https://www.pixiv.net"
    _PIXIV_USER_URL = "https://www.pixiv.net/users"
    _PIXIV_ART_URL  = "https://www.pixiv.net/artworks"
    _PIXIV_AJAX_URL = "https://www.pixiv.net/ajax"

    async def _request(self, url: str, **kwargs) -> BeautifulSoup:
        raise NotImplementedError()

    async def _ajax_request(self, url: str, **kwargs) -> dict:
        raise NotImplementedError()