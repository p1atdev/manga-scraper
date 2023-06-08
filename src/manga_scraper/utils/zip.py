import zipfile
from typing import List
from pathlib import Path

from tqdm import tqdm


def save_as_zip(buffers: List[bytes], path_to_save: str | Path, file_ext: str = ".png"):
    with zipfile.ZipFile(path_to_save, "w") as zip_file:
        with tqdm(total=len(buffers)) as pbar:
            for index, buf in enumerate(buffers):
                # ZIPにバッファから画像を書き込む
                data = zipfile.ZipInfo(f"{index}{file_ext}")
                data.compress_type = zipfile.ZIP_DEFLATED
                zip_file.writestr(data, buf)
                pbar.update(1)
