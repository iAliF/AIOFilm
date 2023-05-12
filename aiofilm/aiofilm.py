from typing import List

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from .exception import AIOFilmException
from .models import Quality, Season


class AIOFilm:
    TIMEOUT = 10
    FILTER_KW = "کیفیت"

    def __init__(self) -> None:
        self._session = requests.Session()

    def find_seasons(self, url: str) -> List[Season]:
        obj = self._get_bs4_object(url)
        dl_section = obj.find("div", {"id": "download_files"})

        qualities = []
        items = []
        last = None

        for index, item in enumerate(dl_section.find_all("li")):
            if not item.has_attr('class'):
                continue

            if 'dliteminfo' in item['class']:
                if last is not None:
                    qualities.append(
                        Season(last, items)
                    )
                    items = []

                last = item.text.strip()
                for to_replace in ("کامل", "دانلود"):
                    last = last.replace(to_replace, "")

            else:
                text = item.find_next("span", {"class": "font-bold"}).text

                if self.FILTER_KW not in text:
                    continue

                href = item.find_next("a")["href"]
                quality = f"{href.split('/')[-1]}p".replace("%20", " ")
                items.append(Quality(quality, href))

        qualities.append(
            Season(last, items)
        )

        return qualities

    def grab_episodes(self):
        ...

    def _get_bs4_object(self, url: str) -> BeautifulSoup:
        try:
            req = self._session.get(url, timeout=self.TIMEOUT)
            if req.status_code != 200:
                raise AIOFilmException(f"Invalid status code ({req.status_code})")

            return BeautifulSoup(req.text, "html.parser")
        except RequestException as err:
            raise AIOFilmException(err)
