import pandas as pd

import scrape, store


def main():
    school_data = pd.DataFrame(None, columns=['Applicants', 'Acceptance Rate', 'Avg HS GPA', 'Selectivity', 'Faculty',
                                              '... w/ Terminal Degree', 'Prof Interest', 'Prof Accessible',
                                              'Grad in 4yrs', '... 5yrs', '... 6yrs', 'Academic Rating', ])
    attributes = ['Applicants', 'Acceptance Rate', 'Average HS GPA', 'Admissions selectivity rating', 'Total Faculty',
                  'with Terminal Degree', 'Professors interesting rating', 'Professors accessible rating',
                  'Graduate in 4 years', 'Graduate in 5 years', 'Graduate in 6 years', 'Academic rating']

    while True:
        try:
            soup, name = scrape.find_school_princeton_page(input("Enter school name: "))
            store.store(soup, name, school_data, attributes)
            print(school_data, '\n')
        except:
            print("Something went wrong. Try again")


main()
