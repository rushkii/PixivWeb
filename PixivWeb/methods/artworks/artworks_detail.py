from PixivWeb.scaffold import Scaffold
from PixivWeb import types

from typing import Dict
import json, dateparser

class GetArtworks(Scaffold):
    async def get_artworks(self, artwork_id: int):
        artwork_id = str(artwork_id)
        res = await self._request(f"{self._PIXIV_ART_URL}/{artwork_id}")
        
        data = json.loads(res.find("meta", {
            "id": "meta-preload-data",
            "name": "preload-data"
        }).attrs.get("content"))
        
        illust: Dict[Dict[str, str], Dict[str, str]] = data['illust'][artwork_id]
        user = data['user'][illust['userId']]
        page = illust["userIllusts"][artwork_id]["pageCount"]
        
        artworks = types.List(
            types.Artworks._parse(
                self,
                id=illust['userIllusts'][i]['id'],
                title=illust['userIllusts'][i]['title'],
                caption=illust['userIllusts'][i]['alt'].split(" - ")[0],
                images={},
                likes_count=0,
                bookmarks_count=0,
                views_count=0,
                comments_count=0,
                page_count=illust['userIllusts'][i]['pageCount'],
                is_animation=illust['illustType'] == 2,
                width=illust['userIllusts'][i]['width'],
                height=illust['userIllusts'][i]['height'],
                sanity_level=illust['userIllusts'][i]['sl'],
                restrict=illust['userIllusts'][i]['restrict'],
                x_restrict=illust['userIllusts'][i]['xRestrict'],
                created_date=dateparser.parse(illust['userIllusts'][i]['createDate']),
                tags=illust['userIllusts'][i]['tags'],
                users=None
            ) for i in illust['userIllusts'].keys()
            if illust['userIllusts'][i] is not None
        )

        return types.Artworks._parse(
            self,
            id=artwork_id,
            title=illust['title'],
            caption=illust['description'],
            images=illust['urls'],
            likes_count=illust['likeCount'],
            bookmarks_count=illust['bookmarkCount'],
            views_count=illust['viewCount'],
            comments_count=illust['commentCount'],
            page_count=page,
            is_animation=illust['illustType'] == 2,
            width=illust['width'],
            height=illust['height'],
            sanity_level=illust['sl'],
            restrict=illust['restrict'],
            x_restrict=illust['xRestrict'],
            created_date=dateparser.parse(illust['createDate']),
            tags=illust["userIllusts"][artwork_id]['tags'],
            users=types.Users._parse(
                self,
                id=user['userId'],
                username=illust['userAccount'],
                name=user['name'],
                is_premium=user['premium'],
                profile_url=f"{self._PIXIV_USER_URL}/{user['userId']}",
                background_image=user['background']['url'] if user.get("background") else None,
                profile_image=user['imageBig'],
                artworks=artworks,
            ),
        )