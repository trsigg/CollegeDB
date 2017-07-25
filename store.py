import re
import numpy as np
import textwrap

import scrape as sc


def clean_num(num_str):
    if not num_str:
        return np.nan

    cleaned_str = re.sub('[$,]', '', num_str.strip())

    if cleaned_str[-1] == '%':
        return float(cleaned_str[:-1]) / 100.

    try:
        return float(cleaned_str)
    except ValueError:
        print(num_str + " not parsed")  # TODO: add context in get_data_by_attrs (handle error there)?
        return np.nan


def find_ratio(num_list):
    if len(num_list) > 1:
        return float(num_list[0]) / float(num_list[1])
    else:
        return np.nan


def store(soup, name, df):
    data = list()

    # Raw data(un-normalized)
    data.extend(sc.get_data_by_attrs(soup, ('Applicants', 'Average HS GPA', 'Total Faculty', 'with Terminal Degree',
                                            'Required Fees', 'Average Cost for Books and Supplies',
                                            'On-Campus Room and Board', 'Comprehensive Fee',
                                            'Registered Student Organizations', 'Number of Honor Societies',
                                            'Number of Social Sororities', 'Number of Religious Organizations',
                                            'Total Undergraduate Enrollment', 'Foreign Countries Represented'),
                                     relationship=lambda tag: tag.parent.find_next_sibling('div'), transform=clean_num))
    data.extend(sc.get_data_by_attrs(soup, ('Starting Median Salary \(Up to', 'Mid-Career Median Salary \(Up to',
                                            'Starting Median Salary \(At least', 'Mid-Career Median Salary \(At least',
                                            'Average Freshman Total', 'Average Undergraduate Total', 'Average Need',
                                            'Average amount of loan', 'Average amount of each'),
                                     relationship=lambda tag: tag.find_next_sibling('div').contents[1],
                                     transform=clean_num, use_re=True))
    data.extend(sc.get_data_by_attrs(soup, (r'Tuition( \(Out|$)',),
                                     relationship=lambda tag: tag.find_next_sibling('div'), transform=clean_num,
                                     use_re=True, tag_type='div'))
    data.extend(sc.get_data_by_attrs(soup, ('Student/Faculty',),
                                     relationship=lambda tag: tag.parent.find_next_sibling('div'),
                                     transform=lambda txt: find_ratio(txt.split(':'))))
    data.extend(sc.get_data_by_attrs(soup, ('Most frequent class size', 'Most frequent lab / sub section size'),
                                     relationship=lambda tag: tag.parent.find_next_sibling('div'),
                                     transform=lambda txt: map(clean_num, txt.split(' - ')), unpack_data=True))


    # Ratings data (60-99)
    data.extend(sc.get_data_by_attrs(soup, ('Admissions selectivity rating', 'Professors interesting rating',
                                            'Professors accessible rating', 'Academic rating', 'Financial Aid Rating',
                                            'Quality of life rating', 'Fire safety rating', 'Green rating',
                                            'Return on Investment (ROI) rating'),
                                     relationship=lambda tag: tag.parent.find_next_sibling('div').contents[0],
                                     transform=lambda txt: (clean_num(txt.strip()[:2]) - 60) / 39, tag_type='a'))


    # Percentage data (0-1)
    data.extend(sc.get_data_by_attrs(soup, ('Acceptance Rate', 'Graduate in 4 years', 'Graduate in 5 years',
                                            'Graduate in 6 years', 'Undergrads living on campus',
                                            'First-Year Students living on campus'),
                                     relationship=lambda tag: tag.find_next_sibling('div'), transform=clean_num,
                                     tag_type='div'))
    data.extend(sc.get_data_by_attrs(soup, ('Undergraduates who have borrowed', 'Percent High Job Meaning',
                                            'Percent STEM'),
                                     relationship=lambda tag: tag.find_next_sibling('div').contents[1],
                                     transform=clean_num, use_re=True))

    print(textwrap.fill(str(list(enumerate(data))), 180))
    # df.loc[name] = data
