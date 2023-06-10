import argparse
import re
from typing import List, Optional, TypedDict, Literal
import json
import requests

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import numpy as np

from ..solver.manga_solver import MangaSolver, MangaImage
from ..downloader.common import Downloader


class EpisodePageItem(TypedDict):
    contentStart: Optional[str]
    height: Optional[int]
    width: Optional[int]
    src: Optional[str]
    type: Literal["main", "other", "backMatter"]


class EpisodePageStructure(TypedDict):
    choJuGiga: Literal["baku"]
    readingDirection: Literal["rtl", "ltr", "ttb"]
    pages: List[EpisodePageItem]


class EpisodeSeriesInfo(TypedDict):
    id: str
    thumbnailUrl: str
    title: str


class EpisodeItem(TypedDict):
    finishReadingNotificationUri: None
    hasPurchased: bool
    id: str
    imageUrisDigest: str
    isPublic: bool  # should be true
    nextReadableProductUri: None
    number: int
    permalink: str
    prevReadableProductUri: Optional[str]
    publishedAt: str
    title: str
    typeName: str  # should be "episode"
    toc: None

    pageStructure: EpisodePageStructure
    series: EpisodeSeriesInfo


class EpisodeDownloader(Downloader):
    solver: MangaSolver

    url: str
    episode: Optional[EpisodeItem] = None

    # https://example.com/episode/12345678901234567890
    # or
    # https://example.com/episode/12345678901234567890.json
    pattern = r"(https://[^/]+/episode/\d+)(\.json)?$"

    def __init__(self, episode_url: str):
        match = self.validate(episode_url)
        if match is not None:
            self.url = self.normalize(match)
        else:
            raise ValueError(f"Invalid episode url: {episode_url}")

    def validate(self, url: str):
        return re.match(self.pattern, url)

    # ~.json に統一
    def normalize(self, match: re.Match[str]):
        return match.group(1) + ".json"

    def _fetch_json(self):
        res = self.fetch(self.url)
        self.episode: EpisodeItem = json.loads(res.text)["readableProduct"]

    def _download_chunk(
        self, chunk: List[EpisodePageItem], solve: bool, pbar: tqdm
    ) -> List[MangaImage]:
        results: List[MangaImage] = []
        for page in chunk:
            if solve:
                answer = self.solver.solve(page["src"])
            else:
                answer = MangaImage(self.solver._load_image(page["src"]).image)
            results.append(answer)
            pbar.update(1)
        return results

    def download(self, threads: int = 4, solve: bool = True) -> List[MangaImage]:
        if self.episode is None:
            self._fetch_json()

        self.solver = MangaSolver()

        # main だけにする
        pages = [
            page
            for page in self.episode["pageStructure"]["pages"]
            if page["type"] == "main"
        ]

        chunks = np.array_split(pages, threads)

        with tqdm(total=len(pages)) as pbar:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for chunk in chunks:
                    futures.append(
                        executor.submit(self._download_chunk, chunk, solve, pbar)
                    )

                results = []
                for future in futures:
                    results.extend(future.result())

        return results
