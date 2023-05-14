from argparse import ArgumentParser
from typing import List, Any

from aiofilm import AIOFilm, Season, Quality
from idm import IDMHelper


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
    parser.add_argument("-f", "--folder", type=str, help="Download path")
    group.add_argument("-p", "--print", action='store_true', help="Print download links")
    group.add_argument("-s", "--save", action='store_true', help="Save download links into file")
    parser.add_argument("-o", "--output", type=str, help="Output file")
    args = parser.parse_args()

    if args.download and args.folder is None:
        parser.error("-d/--download requires --folder")

    if args.save and args.output is None:
        parser.error("-s/--save requires --output")

    aio = AIOFilm()
    seasons = aio.find_seasons(args.url)
    season: Season = get_option("Choose your season", seasons)
    quality: Quality = get_option("Choose your quality", season.qualities)
    episodes = aio.grab_episodes(quality)

    if args.print:
        print(*episodes, sep="\n")

    elif args.download:
        for episode in episodes:
            idm = IDMHelper()
            idm.send_link_to_idm(
                episode.url,
                args.folder,
                episode.name,
                3,
                args.url
            )

    elif args.save:
        with open(args.output, "w") as file:
            file.write("\n".join(ep.url for ep in episodes))


if __name__ == '__main__':
    main()
