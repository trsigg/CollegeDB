import pandas as pd
import numpy as np


def change_nan_to_avg(ser):
    avg = ser.mean()
    new_ser = ser.copy()

    for i, val in ser.iteritems():
        if np.isnan(new_ser[i]):
            new_ser[i] = avg
    return new_ser


def standardize(ser):
    ser_max = ser.max()
    std_avg = ser.mean() / ser_max
    new_ser = pd.Series(index=ser.index)

    for i, val in ser.iteritems():
        if np.isnan(val):
            new_ser[i] = std_avg
        else:
            new_ser[i] = val / ser_max
    return new_ser


def fill_missing_shanghai_data(ser, devs=1.0):
    def_val = ser.min() - devs * ser.std()
    new_ser = ser.copy()

    for i in ser.index:
        if np.isnan(new_ser[i]):
            new_ser[i] = def_val
    return new_ser


def map_to_range(ser, min, max):
    new_ser = pd.Series(index=ser.index)
    diff = max - min

    for i, val in ser.iteritems():
        new_ser[i] = (val - min) / diff
    return new_ser


def create_scoring_db():
    db = pd.HDFStore('database.h5')

    orig_data = db['store']
    score_data = pd.DataFrame(None, columns=('SCORE', '%Faculty w/ Term Degree', 'Req Fees', 'Avg Supply Cst',
                                             'On-Campus Rm&Brd Cst', 'Stdnt Orgs', 'Honor Socs', 'Social Sororities',
                                             'Countries Represented','Init Med Sal (<=B)', 'Mid-Car Med Sal (<=B)',
                                             'Init Med Sal (>=B)', 'Mid-Car Med Sal (>=B)', 'Avg Fresh NBG',
                                             'Avg Udrgd NBG', 'Avg NBL', 'Avg loan debt', 'Avg fresh scholar/grnt pkg',
                                             'Tuition', 'Stdnt/Faculty', 'MstFreq class size (low)', 'Mfcs (high)',
                                             'Selectivity r', 'Prof interest', 'Prof accessible', 'Academic r',
                                             'FinAid r', 'Qual of life', 'Green', 'ROI r', '% Udrgds who have borrowed',
                                             '% High Job Meaning', '% STEM', 'math', 'phys', 'chem', 'earth', 'geo',
                                             'eco', 'mechEng', 'electric', 'automation', 'telecom', 'bioMed', 'compSci',
                                             'civil', 'chemEng', 'materialSci', 'nano', 'energy', 'enviro', 'water',
                                             'biotech', 'aerospace', 'marineEng', 'transport', 'remoteSensing', 'bio',
                                             'humanBio', 'clinicalMed', 'pubHlth', 'medTech', 'pharma', 'econ', 'stats',
                                             'poliSci', 'sociology', 'edu', 'psych', 'finance', 'mngmnt'))

    cols_to_copy = ('Selectivity r', 'Prof interest', 'Prof accessible', 'Academic r', 'FinAid r', 'Qual of life',
                    'Green', 'ROI r', '% Udrgds who have borrowed', '% High Job Meaning', '% STEM')
    cols_to_standardize = ('Req Fees', 'Avg Supply Cst', 'On-Campus Rm&Brd Cst', 'Stdnt Orgs', 'Honor Socs',
                           'Social Sororities', 'Countries Represented', 'Init Med Sal (<=B)', 'Mid-Car Med Sal (<=B)',
                           'Init Med Sal (>=B)', 'Mid-Car Med Sal (>=B)', 'Avg Fresh NBG', 'Avg Udrgd NBG', 'Avg NBL',
                           'Avg loan debt', 'Avg fresh scholar/grnt pkg', 'Tuition', 'Stdnt/Faculty',
                           'MstFreq class size (low)', 'Mfcs (high)')
    shanghai_cols = ('math', 'phys', 'chem', 'earth', 'geo', 'eco', 'mechEng', 'electric', 'automation', 'telecom',
                     'bioMed', 'compSci', 'civil', 'chemEng', 'materialSci', 'nano', 'energy', 'enviro', 'water',
                     'biotech', 'aerospace', 'marineEng', 'transport', 'remoteSensing', 'bio', 'humanBio',
                     'clinicalMed', 'pubHlth', 'medTech', 'pharma', 'econ', 'stats', 'poliSci', 'sociology', 'edu',
                     'psych', 'finance', 'mngmnt')

    for col in cols_to_copy:
        score_data[col] = change_nan_to_avg(orig_data[col])

    for col in cols_to_standardize:
        score_data[col] = standardize(orig_data[col])

    min_score = 500  # bigger than any score in dataset
    max_score = 0
    for col in shanghai_cols:
        new_col = fill_missing_shanghai_data(orig_data[col])
        score_data[col] = new_col

        if min(new_col) < min_score:
            min_score = min(new_col)
        if max(new_col) > max_score:
            max_score = max(new_col)

    # Standardize Shanghai data
    for col in shanghai_cols:
        score_data[col] = map_to_range(score_data[col], min_score, max_score)

    db['scoring'] = score_data
    db.close()


def find_scores():
    db = pd.HDFStore('database.h5')

    score_data = db['scoring']

    importance = (0, 0, -1, -3, -4, 5, 0.5, 0.5, 4, 5, 6, 6, 7, 2, 2, 1, -5, 2, -2, 4, -1, -3, 1, 7, 6, 10, 6, 7, 6, 6,
                  -6, 9, 5, 10, 10, 8, 3, 2, 4, 7, 8, 9, 2, 7, 9, 5, 6, 7, 6, 6, 6, 3, 8, 4, 1, 2, 3, 7, 6, 3, 1, 8, 5,
                  6, 6, 1, 5, 1, 5, 3, 1)

    for i, data in score_data.iterrows():
        score_data.loc[i]['SCORE'] = score_data.loc[i].dot()


find_scores()
