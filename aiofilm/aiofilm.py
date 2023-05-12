from typing import List
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from requests import RequestException

from .exception import AIOFilmException
from .models import Quality, Season, Episode


class AIOFilm:
    TIMEOUT = 10
    FILTER_KW = "کیفیت"
    QUALITY_REPLACE = "دانلود با کیفیت"

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
                quality = text.replace(self.QUALITY_REPLACE, "").strip()
                items.append(Quality(quality, href))

        qualities.append(
            Season(last, items)
        )

        return qualities

    def grab_episodes(self, quality: Quality) -> List[Episode]:
        if AIOFilm.is_movie_url(quality.url):
            return [Episode(quality.quality, quality.url)]

        parse = urlparse(quality.url)
        base = f"{parse.scheme}://{parse.netloc}"

        bs4 = self._get_bs4_object(quality.url)

        episodes = []
        for item in bs4.find_all("li"):

            if not item.has_attr("data-href"):
                continue

            href = item["data-href"]
            if not AIOFilm.is_movie_url(href):
                continue
            href = urljoin(base, href)

            name = item["data-name"].strip()
            episodes.append(Episode(name, href))

        return episodes

    @staticmethod
    def is_movie_url(url: str) -> bool:
        return url.endswith(".mkv")

    def _get_bs4_object(self, url: str) -> BeautifulSoup:
        try:
            req = self._session.get(url, timeout=self.TIMEOUT)
            if req.status_code != 200:
                raise AIOFilmException(f"Invalid status code ({req.status_code})")

            return BeautifulSoup(req.text, "html.parser")
        except RequestException as err:
            raise AIOFilmException(err)
