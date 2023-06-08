import unittest
from src.atom.parser import AtomParser


class TestAtomParser(unittest.TestCase):
    def test_get_atom_feed(self):
        parser = AtomParser("https://shonenjumpplus.com/atom")
        assert parser.feed["feed"]["title"] == "少年ジャンプ＋"

    def parse_manga_atom(self, url: str, site_name: str):
        parser = AtomParser(f"{url}/atom")

        manga_atom = parser.parse()

        assert manga_atom["title"] == site_name
        assert len(manga_atom["entries"]) > 0
        assert manga_atom["entries"][0]["manga_link"]["href"].startswith(
            f"{url}/episode/"
        )
        assert manga_atom["entries"][0]["title"] is not None

    def test_shonenjumpplus_atom(self):
        self.parse_manga_atom("https://shonenjumpplus.com", "少年ジャンプ＋")

    def test_sunday_webry_atom(self):
        self.parse_manga_atom("https://www.sunday-webry.com", "サンデーうぇぶり")

    def test_tonarinoyj_atom(self):
        self.parse_manga_atom("https://tonarinoyj.jp", "となりのヤングジャンプ")


if __name__ == "__main__":
    unittest.main()
