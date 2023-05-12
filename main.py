from argparse import ArgumentParser
from typing import List, Any

from aiofilm import AIOFilm, Season, Quality


def get_option(message: str, iterable: List) -> Any:
    print(
        message,
        *(f"{index + 1}. {item}" for index, item in enumerate(iterable)),
        sep="\n"
    )
    while not ((opt := input("~ ")).isdigit() and 0 < (opt := int(opt)) <= len(iterable)):
        print("Invalid option!")

    return iterable[opt - 1]


def main() -> None:
    parser = ArgumentParser("AIOFilm downloader")
    parser.add_argument("url", help="Movie/Series Url", type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--download", action='store_true', help="Add links to idm")
    group.add_argument("-p", "--print", action='store_true', help="Print download links")
    group.add_argument("-s", "--save", action='store_true', help="Save download links into file")
    args = parser.parse_args()

    aio = AIOFilm()
    seasons = aio.find_seasons(args.url)
    season: Season = get_option("Choose your season", seasons)
    quality: Quality = get_option("Choose your quality", season.qualities)
    episodes = aio.grab_episodes(quality)
    print(*episodes, sep="\n")


if __name__ == '__main__':
    main()
