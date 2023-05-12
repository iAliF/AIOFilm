import sys
from typing import List, Any

from aiofilm import AIOFilm, Season, Quality


def get_option(message: str, iterable: List) -> Any:
    print(
        message,
        *(f"{index + 1}. {item}" for index, item in enumerate(iterable)),
        sep="\n"
    )
    while not ((opt := input("~ ")).isdigit() and 0 < (opt := int(opt)) <= len(seasons)):
        print("Invalid option!")

    return iterable[opt - 1]


url = input("~ Enter your url: ") if len(args := sys.argv) < 2 else args[1]
aio = AIOFilm()
seasons = aio.find_seasons(url)
season: Season = get_option("Choose your season", seasons)
quality: Quality = get_option("Choose your quality", season.qualities)
episodes = aio.grab_episodes(quality)
print(*episodes, sep="\n")
