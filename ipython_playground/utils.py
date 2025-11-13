"""
Utility functions for the ipython-playground package.

This module contains general-purpose utility functions that are useful in 
playground environments for data manipulation, external data fetching, and 
other common tasks.
"""

import re
from urllib.request import urlopen


def read_data_url(url):
    """
    Read a url with json, csv, etc and return the data.

    Helpful for pulling external data for one-off scripts
    """

    # convert start gist URLS to raw URLs
    if re.match(r"https?://gist\.github\.com/", url):
        url = url.replace("gist.github.com", "gist.githubusercontent.com") + "/raw"

    return urlopen(url).read()
