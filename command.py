import scrape as sc
import store as st
from bs4 import BeautifulSoup
from os.path import abspath
import re
import numpy as np
from urllib.request import urlopen, quote
import pandas as pd


def reset(new):
    db = pd.HDFStore('database.h5')

    template = pd.DataFrame(None, columns=('Applicants', 'Avg HS GPA', 'Faculty', 'w/ Term Degree', 'Req Fees',
                                           'Avg Supply Cst', 'On-Campus Rm&Brd Cst', 'Compr Fee', 'Stdnt Orgs',
                                           'Honor Socs', 'Social Sororities', 'Relig Orgs', 'Udrgd Enrollment',
                                           'Countries Represented', 'Init Med Sal (<=B)', 'Mid-Car Med Sal (<=B)',
                                           'Init Med Sal (>=B)', 'Mid-Car Med Sal (>=B)', 'Avg Fresh NBG',
                                           'Avg Udrgd NBG', 'Avg NBL', 'Avg loan debt', 'Avg fresh scholar/grnt pkg',
                                           'Tuition', 'Stdnt/Faculty', 'MstFreq class size (low)', 'Mfcs (high)',
                                           'MstFreq lab/sub-sctn size (low)', 'Mfls (high)', 'Selectivity r',
                                           'Prof interest', 'Prof accessible', 'Academic r', 'FinAid r', 'Qual of life',
                                           'Fire safety', 'Green', 'ROI r', 'Acceptance Rate', 'Grad in 4 years',
                                           '...5 years', '...6 years', 'Udrgds on campus', '1st yr stdnts on campus',
                                           '% Udrgds who have borrowed', '% High Job Meaning', '% STEM', 'math', 'phys',
                                           'chem', 'earth', 'geo', 'eco', 'mechEng', 'electric', 'automation',
                                           'telecom', 'bioMed', 'compSci', 'civil', 'chemEng', 'materialSci', 'nano',
                                           'energy', 'enviro', 'water', 'biotech', 'aerospace', 'marineEng',
                                           'transport', 'remoteSensing', 'bio', 'humanBio', 'clinicalMed', 'pubHlth',
                                           'medTech', 'pharma', 'econ', 'stats', 'poliSci', 'sociology', 'edu', 'psych',
                                           'finance', 'mngmnt'))

    if input('Are you sure you want to overwrite existing data? ') == 'y':
        if not new:
            print('Backing up data...')
            db['bkp'] = db['store']

        if input('Extra sure? ') == 'y':
            db['store'] = template
            if new:
                db['bkp'] = template

    db.close()


def reset2():
    db = pd.HDFStore('database.h5')

    template = pd.DataFrame(None, columns=('SCORE', '%Faculty w/ Term Degree', 'Req Fees', 'Avg Supply Cst',
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

    if input('Are you sure you want to overwrite scoreing db? ') == 'y':
        db['scoring'] = template

    db.close()


def disp():
    db = pd.HDFStore('database.h5')

    print(db)

    if input('\nDisplay data? ') == 'y':
        print('Store:\n', db['store'].to_string())
    if input('Display scoring? ') == 'y':
        print('Backup:\n', db['scoring'].to_string())
    if input('Display backup? ') == 'y':
        print('Backup:\n', db['bkp'].to_string())

    db.close()


def backup(destination='bkp2'):
    db = pd.HDFStore('database.h5')

    if input('Backup <store> to <%s>? ' % destination) == 'y':
        db[destination] = db['store']

    db.close()


# do the thing
disp()

print('Done')
