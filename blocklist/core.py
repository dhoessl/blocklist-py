from requests import get
from re import Pattern

from .errors import (
    LinkNotExistsError
)


class Link:
    def __init__(self, link: str) -> None:
        if link is None:
            raise LinkNotExistsError()
        self.link = link
        self.hosts = []

    def _get_link(self) -> list:
        pass

class LinkCollection:
    def __init__(self, link: str) -> None:
        if link is None:
            raise LinkNotExistsError()
        self.links = self._get_links_from_collection(link)

    def _get_links_from_collection(self, link: str) -> list:
        # Add try except for Timeouts and such
        result = get(link)
        # Some pages might use other formats than text
        # need to check for these too
        return result.text.split()



