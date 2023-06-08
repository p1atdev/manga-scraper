import unittest

from src.downloader.episode import EpisodeDownloader


class TestEpisodeDownloader(unittest.TestCase):
    ok_url = "https://example.com/episode/12345678901234567890"

    def test_validator(self):
        check_list = [
            ["https://example.com/episode/12345678901234567890", True],
            ["https://www.example.jp/episode/12345678901234567890", True],
            ["https://example.com/episode/12345678901234567890.json", True],
            ["https://example.com/episode/12345678901234567890.json.json", False],
            ["https://example.com/episode/12345678901234567890/", False],
            ["https://example.com/episode/12345678901234567890/.json", False],
            ["https://example.com/series", False],
        ]

        def checker(value):
            return value is not None

        for url, expected in check_list:
            dl = EpisodeDownloader(self.ok_url)
            assert checker(dl.validate(url)) == expected

    def test_normalizer(self):
        check_list = [
            [
                "https://example.com/episode/12345678901234567890",
                "https://example.com/episode/12345678901234567890.json",
            ],
            [
                "https://www.example.jp/episode/12345678901234567890",
                "https://www.example.jp/episode/12345678901234567890.json",
            ],
            [
                "https://example.com/episode/12345678901234567890.json",
                "https://example.com/episode/12345678901234567890.json",
            ],
        ]

        for url, expected in check_list:
            dl = EpisodeDownloader(self.ok_url)
            assert dl.normalize(dl.validate(url)) == expected

    def test_fetch_json(self):
        check_list = [
            "https://shonenjumpplus.com/episode/4856001361294191473",
            "https://tonarinoyj.jp/episode/4856001361214474046",
            "https://www.sunday-webry.com/episode/4856001361290357754",
        ]

        for url in check_list:
            dl = EpisodeDownloader(url)

            dl._fetch_json()
            episode = dl.episode

            assert episode is not None
            assert episode["title"] is not None
            assert episode["typeName"] == "episode"
            assert episode["pageStructure"]["pages"] is not None

    def test_download(self):
        check_list = [
            "https://shonenjumpplus.com/episode/4856001361294191473",
            "https://tonarinoyj.jp/episode/4856001361214474046",
            "https://www.sunday-webry.com/episode/4856001361290357754",
        ]

        for url in check_list:
            dl = EpisodeDownloader(url)

            images = dl.download()
            assert len(images) > 0

            assert dl.episode is not None
            assert dl.episode["title"] is not None
            assert dl.episode["typeName"] == "episode"
            assert dl.episode["pageStructure"]["pages"] is not None

            pages = [
                page
                for page in dl.episode["pageStructure"]["pages"]
                if page["type"] == "main"
            ]

            assert len(images) == len(pages)
