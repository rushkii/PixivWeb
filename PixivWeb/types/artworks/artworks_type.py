from PixivWeb.scaffold import Scaffold
from PixivWeb import types
import PixivWeb

from datetime import datetime
from typing import List, Union
import aiofiles, os, asyncio

__all__ = ['Artworks']

class Images(types.Object):
    def __init__(
        self,
        mini: str = None,
        thumb: str = None,
        small: str = None,
        regular: str = None,
        originals: List[str] = None,
    ) -> None:
        self.mini = mini
        self.thumb = thumb
        self.small = small
        self.regular = regular
        self.originals = originals

class Artworks(types.Object, Scaffold):
    def __init__(
        self,
        client: "PixivWeb.Client" = None,
        id: int = None,
        title: str = None,
        caption: str = None,
        images: "Images" = None,
        likes_count: int = None,
        bookmarks_count: int = None,
        views_count: int = None,
        comments_count: int = None,
        page_count: int = None,
        is_animation: bool = None,
        width: int = None,
        height: int = None,
        sanity_level: int = None,
        restrict: str = None,
        x_restrict: str = None,
        created_date: "datetime" = None,
        tags: List[str] = None,
        users: "types.Users" = None,
    ):
        super().__init__(client=client)

        self.id = id
        self.title = title
        self.caption = caption
        self.images = images
        self.likes_count = likes_count
        self.bookmarks_count = bookmarks_count
        self.views_count = views_count
        self.comments_count = comments_count
        self.page_count = page_count
        self.is_animation = is_animation
        self.width = width
        self.height = height
        self.sanity_level = sanity_level
        self.restrict = restrict
        self.x_restrict = x_restrict
        self.created_date = created_date
        self.tags = tags
        self.users = users

    @staticmethod
    def _parse(client, **kwargs) -> "Artworks":
        if kwargs.get("images"):
            originals = []
            for i in range(kwargs.get("page_count")):
                originals.append(f"{kwargs['images']['original'].replace('_p0', f'_p{i}')}")
            images = Images(
                mini=kwargs.get("mini", ""),
                thumb=kwargs.get("thumb", ""),
                small=kwargs.get("small", ""),
                regular=kwargs.get("regular", ""),
                originals=originals,
            )
            kwargs['images'] = images
        return Artworks(client, **kwargs)

    async def download(self, path: str = None) -> Union[str, List[str]]:
        if not path and self._client.download_dir:
            if not os.path.exists(self._client.download_dir):
                os.mkdir(self._client.download_dir)
            path = self._client.download_dir
        
        elif path and not self._client.download_dir:
            path = path
        
        elif not path and not self._client.download_dir:
            if not os.path.exists("downloads"):
                os.mkdir("downloads")
            path = "downloads"
        
        paths = []
        imbytes = []
        
        async def _handle_dl(img):
            return await self._client._download_request(img)

        for img in self.images.originals:
            imbytes.append(asyncio.ensure_future(_handle_dl(img)))

        imbytes = await asyncio.gather(*imbytes)
        
        async def _handle_save(i):
            async with aiofiles.open(f"{path}/{self.id}_{i}.jpg", 'wb') as f:
                await f.write(imbytes[i])
            return f"{path}/{self.id}_{i}.jpg"

        for i in range(len(imbytes)):
            paths.append(asyncio.ensure_future(_handle_save(i)))
        
        paths = await asyncio.gather(*paths)
        
        return paths