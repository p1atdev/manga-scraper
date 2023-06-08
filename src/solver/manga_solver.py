import cv2u
import cv2
import numpy as np


class MangaImage:
    image: np.ndarray

    def __init__(self, image: np.ndarray):
        self.image = image

    def buffer(self, ext: str = ".png") -> bytes:
        return cv2.imencode(ext, self.image)[1].tobytes()


class MangaPuzzle:
    image: np.ndarray
    height: int
    width: int
    cell_width: int
    cell_height: int

    DIVIDE_NUM = 4
    MULTIPLE = 8

    def __init__(self, image_path_or_url: str):
        if image_path_or_url.startswith("http"):
            self.image = cv2u.urlread(image_path_or_url)
        else:
            self.image = cv2.imread(image_path_or_url)

        self.height, self.width = self.image.shape[:2]
        self.cell_width = (
            self.width // (self.DIVIDE_NUM * self.MULTIPLE)
        ) * self.MULTIPLE
        self.cell_height = (
            self.height // (self.DIVIDE_NUM * self.MULTIPLE)
        ) * self.MULTIPLE


class MangaSolver:
    def _load_image(self, image_path_or_url: str) -> MangaPuzzle:
        return MangaPuzzle(image_path_or_url)

    def solve(self, image_path_or_url: str) -> MangaImage:
        puzzle = self._load_image(image_path_or_url)

        for i in range(puzzle.DIVIDE_NUM):
            for j in range(i + 1):
                # swap
                (
                    puzzle.image[
                        j * puzzle.cell_height : (j + 1) * puzzle.cell_height,
                        i * puzzle.cell_width : (i + 1) * puzzle.cell_width,
                    ],
                    puzzle.image[
                        i * puzzle.cell_height : (i + 1) * puzzle.cell_height,
                        j * puzzle.cell_width : (j + 1) * puzzle.cell_width,
                    ],
                ) = (
                    puzzle.image[
                        i * puzzle.cell_height : (i + 1) * puzzle.cell_height,
                        j * puzzle.cell_width : (j + 1) * puzzle.cell_width,
                    ].copy(),
                    puzzle.image[
                        j * puzzle.cell_height : (j + 1) * puzzle.cell_height,
                        i * puzzle.cell_width : (i + 1) * puzzle.cell_width,
                    ].copy(),
                )

        return MangaImage(puzzle.image)
