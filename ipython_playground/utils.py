import re
from urllib.request import urlopen

def read_data_url(url: str) -> str:
    """
    Read a url with json, csv, etc and return the data as a decoded string.

    Helpful for pulling external data for one-off scripts.
    """
    if re.match(r"https?://gist\.github\.com/", url):
        url = url.replace("gist.github.com", "gist.githubusercontent.com") + "/raw"

    with urlopen(url) as response:
        return response.read().decode("utf-8")
