import zipfile
from typing import List
from pathlib import Path


def save_as_zip(buffers: List[bytes], path_to_save: str | Path, file_ext: str = ".png"):
    with zipfile.ZipFile(path_to_save, "w") as zip_file:
        for index, buf in enumerate(buffers):
            # ZIPにバッファから画像を書き込む
            data = zipfile.ZipInfo(f"{index}{file_ext}")
            data.compress_type = zipfile.ZIP_DEFLATED
            zip_file.writestr(data, buf)
