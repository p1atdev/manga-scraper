import re
from typing import TypedDict
import requests

from ..utils.user_agent import USER_AGENT


class Downloader:
    def __init__(self) -> None:
        pass

    def validate(self, url: str):
        raise NotImplementedError()

    def normalize(self, match: re.Match[str]):
        raise NotImplementedError()

    def fetch(self, url: str):
        headers = {
            "User-Agent": USER_AGENT["Firefox"],
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
        }
        res = requests.get(url, headers=headers)
        if not res.ok:
            raise ValueError(f"Failed to fetch: {url}. status_code={res.status_code}")
        return res
