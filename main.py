import pandas as pd
import numpy as np
from os.path import abspath

import scrape as sc
import store as st


def main():
    subjects = ('math', 'phys', 'chem', 'earth', 'geo', 'eco', 'mechEng', 'electric', 'automation', 'telecom', 'bioMed',
                'compSci', 'civil', 'chemEng', 'materialSci', 'nano', 'energy', 'enviro', 'water', 'biotech',
                'aerospace', 'marineEng', 'transport', 'remoteSensing', 'bio', 'humanBio', 'clinicalMed', 'pubHlth',
                'medTech', 'pharma', 'econ', 'stats', 'poliSci', 'sociology', 'edu', 'psych', 'finance', 'mngmnt')

    db = pd.HDFStore('database.h5')

    print(db)

    school_data = db['store']

    def get_user_action():
        print(school_data.to_string())
        saved = False

        if input('Save data? ') != 'n':
            db['store'] = school_data
            saved = True

        if input('Quit? ') == 'y':
            if not saved:
                if input('Sure you don\'t want to save? ') != 'y':
                    db['store'] = school_data
            if input('Really quit? ') == 'y':
                db.close()
                exit()

    for sub in subjects:
        try:
            print('\nLoading Shanghai %s data' % sub)
            shanghai = sc.get_soup(r'file:\\' + abspath('Shanghai Rankings\%s.html' % sub))
            table = shanghai.find('table', id='UniversityRanking')('tr', limit=50)[1:]
        except:
            print('Failed.')
            get_user_action()

        for row in table:
            data = row('td')
            country = data[2].img['title']

            if country in ('United States', 'Canada', 'United Kingdom'):
                if data[1].a:
                    name = data[1].a.string
                else:
                    name = data[1].string

                if country != 'United States':
                    school_data.loc[name] = [np.nan] * len(school_data.columns)
                    print('%s (%s) added.' % (name, country))
                elif name not in school_data.index:
                    soup = sc.find_school_princeton_page(name)
                    if soup:
                        st.store(soup, name, school_data)
                    else:
                        print('Match for %s not found.' % name)
                        get_user_action()

                try:
                    school_data.loc[name][sub] = float(data[3].string)
                except ValueError:
                    print('Failed to store subject score for %s.' % name)
                    get_user_action()

        get_user_action()


main()
