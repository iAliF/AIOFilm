from dataclasses import dataclass
from typing import List


@dataclass
class Quality:
    quality: str
    url: str

    def __str__(self) -> str:
        return self.quality


@dataclass()
class Season:
    name: str
    qualities: List[Quality]

    def __str__(self) -> str:
        return self.name
