# AIOFilm

**AIOFilm** is a simple Python script to extract the AIOFilm website episodes link You can **save** them into a file, **add** them to the IDM download queue, or just see them in the console

## How to install

1. setup your **virtual environment**
2. install **requirements** using `pip install -r requirements.txt`

## Usage

```
usage: python main.py [-h] [-d] [-f FOLDER] [-p] [-s] [-o OUTPUT] url

positional arguments:
  url                   Movie/Series Url

options:
  -h, --help            show this help message and exit
  -d, --download        Add links to idm
  -f FOLDER, --folder FOLDER
                        Download path
  -p, --print           Print download links
  -s, --save            Save download links into a file
  -o OUTPUT, --output OUTPUT
                        Output file
```

## Resources

[python-idm-helper](https://github.com/zackmark29/python-idm-helper)
