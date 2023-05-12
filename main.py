import sys
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

url = input("~ Enter your url: ") if len(args := sys.argv) < 2 else args[1]
data = requests.get(url).text
bs4 = BeautifulSoup(data, "html.parser")

qualities = []

print("Choose your quality:")
for index, item in enumerate(bs4.find_all("li", {"class": "dlitems"})):
    link = item.find_next("a")["href"]
    quality = f"{link.split('/')[-1]}p"
    print(f"{index + 1}. {quality}")
    qualities.append(link)

quality = input("~ ")
if not (quality.isdigit() and 0 < (quality := int(quality)) <= len(qualities)):
    print("Invalid option!")
    exit()

link = qualities[quality - 1]

parse = urlparse(link)
base = f"{parse.scheme}://{parse.netloc}"

data = requests.get(link).text
bs4 = BeautifulSoup(data, "html.parser")

for item in bs4.find_all("li"):
    try:
        name = item["data-name"]
        href = urljoin(base, item["data-href"])
        if not href.endswith(".mkv"):
            continue
        print(name, href, sep=" | ")
    except KeyError:
        pass

