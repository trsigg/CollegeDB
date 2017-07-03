import re
import numpy as np

import scrape as sc


def clean_num(num_str):
    if not num_str:
        return np.nan

    cleaned_str = re.sub(',', '', num_str.strip())

    if cleaned_str[-1] == '%':
        return float(cleaned_str[:-1]) / 100.

    try:
        return float(cleaned_str)
    except ValueError:
        print(num_str + " not parsed")  # TODO: add context in store (handle error there)?
        return np.nan


def get_data_by_attrs(soup, attrs):
    data = list()
    for attr in attrs:
        tag = soup.find(text=attr).find_next_sibling('div')
        if tag and tag.string:
            data.append(tag.string)
        else:
            data.append(None)
    return data


def get_ratings_data(soup, attrs):
    ''' 60-99 '''
    data = list()
    for attr in attrs:
        tag = soup.find('a', text=attr).parent.find_next_sibling(class_='number-callout')
        data.append((clean_num(tag.string) - 60) / 39)    # TODO: ensure existence?
    return data


def get_percent_data(soup, attrs):
    ''' 0-1 '''
    data = list()
    for datum in get_data_by_attrs(soup, attrs):
        if datum:
            data.append(clean_num(datum))
        else:
            data.append(np.nan)
    return data


def store(soup, name, df):
    data = list()

    # Ratings data (60-99)
    data.extend(get_ratings_data(soup, ('Admissions selectivity rating', 'Professors interesting rating',
                                        'Professors accessible rating', 'Academic rating', 'Financial Aid Rating',
                                        'Quality of life rating', 'Fire safety rating', 'Green rating',
                                        'Return on Investment (ROI) rating')))

    # Percentage data (0-1)
    data.extend(get_percent_data(soup, ('Acceptance Rate', 'Graduate in 4 years', 'Graduate in 5 years',
                                        'Graduate in 6 years', )))

    data.extend(get_attr_accessible_data(soup, ('Applicants', 'Average HS GPA',
                                                'Total Faculty',
                                                'with Terminal Degree', )))

    # Get GPA distribution stats
    dist = list()
    gpa_div = sc.nth_sibling(sc.find_tag_with_contents(soup, 'GPA Breakdown').parent, 2)    # TODO: ensure existence
    for div in gpa_div.contents[1:-1:2]:
        dist.append(clean_num(div.contents[1].string))
    data.append(dist)

    print(data)
    # df.loc[name] = data
