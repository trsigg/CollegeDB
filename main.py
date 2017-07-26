import pandas as pd

import scrape as sc
import store as st


def main():
    ''' school_data = pd.DataFrame(None, columns=('Applicants', 'Avg HS GPA', 'Faculty', 'w/ Term Degree', 'Req Fees',
                                              'Avg Supply Cst', 'On-Campus Rm&Brd Cst', 'Compr Fee', 'Stdnt Orgs',
                                              'Honor Socs', 'Social Sororities', 'Relig Orgs', 'Udrgd Enrollment',
                                              'Countries Represented', 'Init Med Sal (<=B)', 'Mid-Car Med Sal (<=B)',
                                              'Init Med Sal (>=B)', 'Mid-Car Med Sal (>=B)', 'Avg Fresh NBG',
                                              'Avg Udrgd NBG', 'Avg NBL', 'Avg loan debt', 'Avg fresh scholar/grnt pkg',
                                              'Tuition', 'Stdnt/Faculty', 'MstFreq class size (low)', 'Mfcs (high)',
                                              'MstFreq lab/sub-sctn size (low)', 'Mfls (high)', 'Selectivity r',
                                              'Prof interest', 'Prof accessible', 'Academic r', 'FinAid r',
                                              'Qual of life', 'Fire safety', 'Green', 'ROI r', 'Acceptance Rate',
                                              'Grad in 4 years', '...5 years', '...6 years', 'Udrgds on campus',
                                              '1st yr stdnts on campus', '% Udrgds who have borrowed',
                                              '% High Job Meaning', '% STEM')) '''

    db = pd.HDFStore('test1.h5')

    print(db)

    school_data = db['t2']

    while True:
        try:
            soup, name = sc.find_school_princeton_page(input("Enter school name: "))
            st.store(soup, name, school_data)
            print(school_data.to_string(), '\n')
        except:
            if input("Something went wrong. Do you want to quit and save the database? ") == 'y':
                db['t2'] = school_data
                db.close()
                print("Database updated. Exiting.", db)
                break


main()
