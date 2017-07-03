import pandas as pd

import scrape, store


def main():
    '''school_data = pd.DataFrame(None, columns=['Applicants', 'Acceptance Rate', 'Avg HS GPA', 'Selectivity', 'Faculty',
                                              '... w/ Terminal Degree', 'Prof Interest', 'Prof Accessible',
                                              'Grad in 4yrs', '... 5yrs', '... 6yrs', 'Academic Rating', ])'''

    db = pd.HDFStore('test1.h5')

    print(db)

    school_data = db['t1']

    attributes = ['Applicants', 'Acceptance Rate', 'Average HS GPA', 'Admissions selectivity rating', 'Total Faculty',
                  'with Terminal Degree', 'Professors interesting rating', 'Professors accessible rating',
                  'Graduate in 4 years', 'Graduate in 5 years', 'Graduate in 6 years', 'Academic rating']

    while True:
        try:
            soup, name = scrape.find_school_princeton_page(input("Enter school name: "))
            store.store(soup, name, school_data, attributes)
            print(school_data, '\n')
        except:
            if input("Something went wrong. Do you want to quit and save the database? ") == 'y':
                db['t1'] = school_data
                db.close()
                print("Database updated. Exiting.", db)
                break


main()
