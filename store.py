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


def store(soup, name, df):
    data = list()

    # Ratings data (60-99)
    data.extend(sc.get_data_by_attrs(soup, ('Admissions selectivity rating', 'Professors interesting rating',
                                            'Professors accessible rating', 'Academic rating', 'Financial Aid Rating',
                                            'Quality of life rating', 'Fire safety rating', 'Green rating',
                                            'Return on Investment (ROI) rating'),
                                     relationship=lambda tag: tag.parent.find_next_sibling(class_='number-callout'),
                                     transform=lambda txt: (clean_num(txt) - 60) / 39, tag_type='a'))

    # Percentage data (0-1)
    data.extend(sc.get_data_by_attrs(soup, ('Acceptance Rate', 'Graduate in 4 years', 'Graduate in 5 years',
                                            'Graduate in 6 years'),
                                     relationship=lambda tag: tag.parent.find_next_sibling('div'), transform=clean_num))

    # ('Applicants', 'Average HS GPA', 'Total Faculty', 'with Terminal Degree')

    # Get GPA distribution stats
    dist = list()
    gpa_header = soup.find(text='GPA Breakdown')
    if gpa_header:
        for tag in gpa_header.parent.parent.find_next_sibling('div').find_all(class_='col-xs-2 col-sm-2 bold'):
            dist.append(clean_num(tag.string))  # TODO: Ensure existence?
        data.append(dist)

    print(data)
    # df.loc[name] = data
