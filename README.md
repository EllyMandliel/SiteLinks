# SiteLinks
Asynchronous link-scraper.
This is a small project intended to allow scraping all the the links off a website, mostly useful for CTFs.

## Installaion
Run the following:
```shell script
$ python3 -m pip install SiteLinks 
```
and we're good to go.
## Usage:
To use the script simply run:
```
$ python -m SiteLinks [--depth] [-s] [-o] hostname
```
#### Flags:
+ -s - Include search status (usually a longer run)
+ -o - Include links outside the host.