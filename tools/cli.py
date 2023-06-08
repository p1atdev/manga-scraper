import argparse
from pathlib import Path
from typing import List

from manga_scraper.downloader.episode import EpisodeDownloader
from manga_scraper.utils.zip import save_as_zip


from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("--output", "-o", type=str)
    parser.add_argument(
        "--zip", "-z", action="store_true", default=False, help="Save as zip"
    )
    parser.add_argument(
        "--download_threads",
        type=int,
        default=4,
        help="Number of threads to download pages",
    )
    parser.add_argument(
        "--image_ext",
        type=str,
        default=".png",
        help="Extension of image file to save",
    )

    return parser.parse_args()


def save_to_folder(
    buffers: List[bytes], path_to_save: str | Path, file_ext: str = ".png"
):
    path_to_save = Path(path_to_save)
    path_to_save.mkdir(parents=True, exist_ok=True)

    with tqdm(total=len(buffers)) as pbar:
        for index, buf in enumerate(buffers):
            with open(path_to_save / f"{index}{file_ext}", "wb") as f:
                f.write(buf)
            pbar.update(1)


def main():
    args = parse_args()

    # TODO: 渡されたURLが本当にepisodeのURLかをチェックして分岐
    print("Episode URL: ", args.url)

    print("Downloading...")
    dl = EpisodeDownloader(args.url)
    pages = [page.buffer() for page in dl.download()]
    print("Downloaded!")

    print("Saving...")

    output_path = args.output
    if output_path is None:
        manga_title = dl.episode["title"]
        output_path = Path("./") / manga_title
    else:
        output_path = Path(output_path)

    if args.zip:
        save_as_zip(pages, output_path, file_ext=".png")
    else:
        save_to_folder(pages, output_path, file_ext=".png")

    print("Saved!")
    print("All done!")


if __name__ == "__main__":
    main()
