from PixivWeb.scaffold import Scaffold
from PixivWeb import types
import PixivWeb

from typing import List

class Users(types.Object, Scaffold):
    def __init__(
        self,
        client: "PixivWeb.Client" = None,
        id: int = None,
        username: str = None,
        name: str = None,
        is_premium: bool = None,
        profile_url: str = None,
        background_image: str = None,
        profile_image: str = None,
        artworks: List["types.Artworks"] = None,
    ) -> None:
        super().__init__(client=client)

        self.id = id
        self.username = username
        self.name = name
        self.is_premium = is_premium
        self.profile_url = profile_url
        self.background_image = background_image
        self.profile_image = profile_image
        self.artworks = artworks

    @staticmethod
    def _parse(client, **kwargs) -> "Users":
        return Users(client, **kwargs)