from requests import get, ConnectTimeout
from re import compile
from loguru import logger
from os import path
from datetime import datetime, UTC

from .errors import (
    LinkNotExistsError
)


def get_entries_from_link(link: str) -> list:
    try:
        result = get(link, timeout=(3, 20))
    except ConnectTimeout:
        logger.warning(f"Link {link} no accessible")
        return []
    # Some pages might use other formats than text
    # need to check for these too
    return result.text.split("\n")


class Link:
    def __init__(self, link: str) -> None:
        if link is None:
            raise LinkNotExistsError()
        self.link = link
        self.hosts = []

    def get_domains(self) -> None:
        pattern = compile(
            r'^.*?(([a-zA-Z0-9-]+\.){1,}[a-zA-Z]{2,}).*?$'
        )
        if not self.link:
            return None
        logger.info(f"Fetching entries from {self.link}")
        entries = get_entries_from_link(self.link)
        if not entries:
            return None
        for entry in entries:
            if (
                entry.startswith("#") or entry.startswith("!")
                or entry in [" ", ""]
                or entry.encode()[:3] == b'\xef\xbb\xbf'
            ):
                continue
            pattern_match = pattern.search(entry)
            if (
                not pattern_match
                or not pattern_match.group(1)
                or pattern_match.group(1) == "localhost.localdomain"
            ):
                continue
            self.hosts.append(pattern_match.group(1))


class LinkCollection:
    def __init__(self, link: str) -> None:
        if link is None:
            raise LinkNotExistsError()
        logger.info(f"Collection: {link}")
        self.link = link
        self.links = self._get_link_list(link)
        self.hosts = []

    def _get_link_list(self, input_link: str) -> None:
        link_list = []
        for link in get_entries_from_link(input_link):
            link_list.append(Link(link))
        return link_list

    def run(self) -> None:
        for link in self.links:
            link.get_domains()
            self.hosts += link.hosts
        logger.info(
            f"All entries: {len(self.hosts)} - "
            f"Uniq: {len(sorted(set(self.hosts)))}"
        )
        self.hosts = sorted(set(self.hosts))

    def save_to_file(self, file: str = "/tmp/hosts.txt") -> None:
        if not path.isdir(path.split(file)[0]):
            raise FileNotFoundError(
                "Directory {path.split(file)[0]} does not exist"
            )
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S %z")
        with open(file, "w") as fp:
            fp.write(
                "# Autmoatic generated list of hosts to use on a pihole "
                f"- Created: {now}\n"
                f"# Collection: {self.link}\n"
                f"{'\n'.join(self.hosts)}"
            )
