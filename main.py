import sys
from typing import List, Any

from aiofilm import AIOFilm, Season, Quality

url = input("~ Enter your url: ") if len(args := sys.argv) < 2 else args[1]


def get_option(message: str, iterable: List) -> Any:
    print(
        message,
        *(f"{index + 1}. {item}" for index, item in enumerate(iterable)),
        sep="\n"
    )
    while not ((opt := input("~ ")).isdigit() and 0 < (opt := int(opt)) <= len(seasons)):
        print("Invalid option!")

    return iterable[opt - 1]


aio = AIOFilm()
seasons = aio.find_seasons(url)
season: Season = get_option("Choose your season", seasons)
quality: Quality = get_option("Choose your quality", season.qualities)
print(quality.url)

# parse = urlparse(link)
# base = f"{parse.scheme}://{parse.netloc}"
#
# data = requests.get(link).text
# bs4 = BeautifulSoup(data, "html.parser")
#
# for item in bs4.find_all("li"):
#     try:
#         name = item["data-name"]
#         href = urljoin(base, item["data-href"])
#         if not href.endswith(".mkv"):
#             continue
#         print(name, href, sep=" | ")
#     except KeyError:
#         pass
#
#
