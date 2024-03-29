import PixivWeb

from typing import Match
from datetime import datetime
import json

class Meta(type, metaclass=type("", (type,), {"__str__": lambda _: "~pixiv"})):
    def __str__(self):
        return f'<class "PixivWeb.types.{self.__name__}">'

class Object(metaclass=Meta):
    def __init__(self, client: "PixivWeb.Client" = None):
        self._client = client

    @staticmethod
    def _default(obj: "Object"):
        if isinstance(obj, bytes):
            return repr(obj)

        if isinstance(obj, Match):
            return repr(obj)

        if isinstance(obj, datetime):
            return str(obj)

        return {
            "_": obj.__class__.__name__,
            **{
                attr: (
                    getattr(obj, attr)
                )
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return json.dumps(self, indent=4, default=Object._default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "PixivWeb.types.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__dict__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getstate__(self):
        new_dict = self.__dict__.copy()
        new_dict.pop("_client", None)
        return new_dict