import cv2u
import cv2
import numpy as np


class MangaSolver:
    manga_image: np.ndarray
    height: int
    width: int
    cell_width: int
    cell_height: int

    DIVIDE_NUM = 4
    MULTIPLE = 8

    def __init__(self, manga_path_or_url: str):
        if manga_path_or_url.startswith("http"):
            self.manga_image = cv2u.urlread(manga_path_or_url)
        else:
            self.manga_image = cv2.imread(manga_path_or_url)

        self.height, self.width = self.manga_image.shape[:2]
        self.cell_width = (
            self.width // (self.DIVIDE_NUM * self.MULTIPLE)
        ) * self.MULTIPLE
        self.cell_height = (
            self.height // (self.DIVIDE_NUM * self.MULTIPLE)
        ) * self.MULTIPLE

    def solve(self):
        for i in range(self.DIVIDE_NUM):
            for j in range(i + 1):
                # swap
                (
                    self.manga_image[
                        j * self.cell_height : (j + 1) * self.cell_height,
                        i * self.cell_width : (i + 1) * self.cell_width,
                    ],
                    self.manga_image[
                        i * self.cell_height : (i + 1) * self.cell_height,
                        j * self.cell_width : (j + 1) * self.cell_width,
                    ],
                ) = (
                    self.manga_image[
                        i * self.cell_height : (i + 1) * self.cell_height,
                        j * self.cell_width : (j + 1) * self.cell_width,
                    ].copy(),
                    self.manga_image[
                        j * self.cell_height : (j + 1) * self.cell_height,
                        i * self.cell_width : (i + 1) * self.cell_width,
                    ].copy(),
                )

    def buffer(self, ext: str = ".png") -> bytes:
        return cv2.imencode(ext, self.manga_image)[1].tobytes()
