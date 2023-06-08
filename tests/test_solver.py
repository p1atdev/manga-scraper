import unittest
from src.solver.manga_solver import MangaSolver
import cv2
from pathlib import Path

output_path = Path("./tests/assets/out").resolve()
output_path.mkdir(parents=True, exist_ok=True)


class TestMangaSolver(unittest.TestCase):
    def test_read_image_0(self):
        path = Path("./tests/assets/0-q.jpg").resolve()
        assert path.exists()

        img = cv2.imread(str(path))
        assert img is not None

    def test_solve_image_0(self):
        solver = MangaSolver()
        img = solver.solve("./tests/assets/0-q.jpg")
        assert img.buffer() is not None

    def test_write_out_image_0(self):
        solver = MangaSolver()
        img = solver.solve("./tests/assets/0-q.jpg")

        path = Path("./tests/assets/out/0.jpg").resolve()
        cv2.imwrite(str(path), img.image)

    def test_compare_answer_image_0(self):
        solver = MangaSolver()
        img = solver.solve("./tests/assets/0-q.jpg")

        answer = cv2.imread("./tests/assets/0-a.jpg")
        assert answer is not None

        assert (img.image == answer).all()


if __name__ == "__main__":
    unittest.main()
