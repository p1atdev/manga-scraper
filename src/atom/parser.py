import feedparser
from .manga_atom import MangaAtom, MangaEntry, MangaLink, MangaThumbLink


class AtomParser:
    def __init__(self, url):
        self.url = url
        self.feed = feedparser.parse(self.url)

    def parse(self) -> MangaAtom:
        feed = self.feed["feed"]

        atom: MangaAtom = {
            "title": feed["title"],
            "subtitle": feed["subtitle"],
            "updated": feed["updated"],
            "id": feed["id"],
            "link": feed["link"],
            "entries": [],
        }

        entries = []

        for entry in self.feed["entries"]:
            links = entry["links"]
            manga_link: MangaLink = None
            manga_thumb_link: MangaThumbLink = None

            for link in links:
                if link["rel"] == "alternate":
                    manga_link = link
                elif link["rel"] == "enclosure":
                    manga_thumb_link = link

            manga_entry: MangaEntry = {
                "title": entry["title"],
                "manga_link": manga_link,
                "manga_thumb_link": manga_thumb_link,
                "id": entry["id"],
                "updated": entry["updated"],
                "content": entry["content"],
                "author": entry["author"],
            }

            entries.append(manga_entry)

        atom["entries"] = entries

        return atom
