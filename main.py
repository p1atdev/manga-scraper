from src.atom.parser import AtomParser


parser = AtomParser("https://shonenjumpplus.com/atom")

print(parser.feed["entries"])

manga_atom = parser.parse()

assert manga_atom["title"] == "少年ジャンプ＋"
