import pandas as pd

import scrape as sc
import store as st


def main():
    ''' school_data = pd.DataFrame(None, columns=['Applicants', 'Acceptance Rate', 'Avg HS GPA', 'Selectivity', 'Faculty',
                                              '... w/ Terminal Degree', 'Prof Interest', 'Prof Accessible',
                                              'Grad in 4yrs', '... 5yrs', '... 6yrs', 'Academic Rating', ]) '''

    db = pd.HDFStore('test1.h5')

    print(db)

    school_data = db['t1']

    while True:
        try:
            soup, name = sc.find_school_princeton_page(input("Enter school name: "))
            st.store(soup, name, school_data)
            # print(school_data, '\n')
        except:
            if input("Something went wrong. Do you want to quit and save the database? ") == 'y':
                db['t1'] = school_data
                db.close()
                print("Database updated. Exiting.", db)
                break


main()
