import re
import numpy as np

import scrape


def clean_num(num_str):
    cleaned_str = re.sub(',', '', num_str)

    if num_str[-1] == '%':
        return float(num_str[:-1]) / 100.

    try:
        return float(cleaned_str)
    except ValueError:
        print(num_str + " not parsed")  # TODO: add context in store (handle error there)?
        return np.nan


def store(soup, name, df, attr_names):
    data = list()
    for attr in attr_names:
        tag = scrape.get_tag_after(soup, attr)

        if tag and tag.string:
            data.append(clean_num(tag.string))
        else:
            data.append(np.nan)
    df.loc[name] = data
