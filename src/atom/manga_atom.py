from typing import TypedDict, List


class MangaLink(TypedDict):
    href: str
    rel: str


class MangaThumbLink(TypedDict):
    href: str
    rel: str
    length: str
    type: str


class MangaEntry(TypedDict):
    title: str
    manga_link: MangaLink
    manga_thumb_link: MangaThumbLink
    id: str
    updated: str
    content: dict[str, str]
    author: str


class MangaAtom(TypedDict):
    title: str
    subtitle: str
    updated: str
    id: str
    link: str
    entries: List[MangaEntry]
