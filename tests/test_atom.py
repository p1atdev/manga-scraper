import unittest
from src.atom.parser import AtomParser


class TestAtomParser(unittest.TestCase):
    def test_get_atom_feed(self):
        parser = AtomParser("https://shonenjumpplus.com/atom")
        assert parser.feed["feed"]["title"] == "少年ジャンプ＋"

    def test_parse_manga_atom(self):
        parser = AtomParser("https://shonenjumpplus.com/atom")

        manga_atom = parser.parse()

        assert manga_atom["title"] == "少年ジャンプ＋"
        assert len(manga_atom["entries"]) > 0
        assert manga_atom["entries"][0]["manga_link"]["href"].startswith(
            "https://shonenjumpplus.com/episode/"
        )
        assert manga_atom["entries"][0]["title"] is not None


if __name__ == "__main__":
    unittest.main()
