import unittest
from pathlib import Path

from manga_scraper.utils.zip import save_as_zip

import cv2


class TestUtils(unittest.TestCase):
    def test_save_images_as_zip(self):
        ext = ".jpg"
        files = ["./tests/assets/0-q.jpg", "./tests/assets/0-a.jpg"]
        images = [cv2.imread(file) for file in files]
        buffers = []
        for image in images:
            success, buffer = cv2.imencode(ext, image)
            if success:
                buffers.append(buffer)

        assert len(buffers) == 2

        zip_path = "./tests/assets/out/zip0.zip"

        save_as_zip(buffers, zip_path, ext)

        assert Path(zip_path).exists()


if __name__ == "__main__":
    unittest.main()
