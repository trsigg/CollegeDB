from bs4 import BeautifulSoup
from urllib.request import urlopen, quote
import numpy as np
import re


def get_soup(url):
    # print(url)
    return BeautifulSoup(urlopen(url), 'lxml')


def format_name(name):
    return re.sub('(, )|(--)|( - )|( at )', ' ',
                  re.sub('University of California(, )|(--)', 'uc ',
                         name.replace('The ', '')))


def find_school_princeton_page(name):
    formatted_name = format_name(name)
    soup = get_soup('https://www.princetonreview.com/college-search?search=' + quote(formatted_name))
    prompt_str = 'Does %s match ' % name

    if soup.find(class_='school-headline'):  # redirected straight to school page
        print(name + ' added.')
        return soup
    else:  # Page returned is search page
        for poss_heading in soup('h2', class_='margin-top-none'):
            poss_link = poss_heading.a
            poss_name = poss_link.string

            if format_name(poss_name) == formatted_name:
                print(name + ' added.')
                return get_soup('https://www.princetonreview.com' + poss_link['href'])
            elif input(prompt_str + poss_name + '? ') == 'y':
                return get_soup('https://www.princetonreview.com' + poss_link['href'])
            else:
                prompt_str = '  ...'

        query = input('No more choices available for %s. Enter alternative query: ' % name)
        if query == 'n':
            return None
        else:
            return find_school_princeton_page(query)


def identity(x):
    return x


def unpack(obj):
    if hasattr(obj, '__iter__'):
        lst = list()
        for x in obj:
            lst.extend(unpack(x))
        return lst
    else:
        return [obj]


def tag_text_matches(pattern, tag_type=None):
    def matches(tag):
        if tag and tag.string and (tag_type is None or tag.name == tag_type):
            return re.search(pattern, tag.string)
        return False

    return matches


def get_data_by_attrs(soup, attrs, relationship=identity, transform=identity, default=np.nan, tag_type=None,
                      use_re=False, unpack_data=False):
    data = list()
    for attr in attrs:
        if use_re:
            header = soup.find(tag_text_matches(attr, tag_type))
        else:
            header = soup.find(tag_type, text=attr)

        if header:  # TODO: try/except?
            tag = relationship(header)
            if tag and tag.string:
                data.append(transform(tag.string))
            else:
                data.append(default)
        else:
            data.append(default)

    if unpack_data:
        return unpack(data)

    return data
