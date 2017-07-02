import pandas as pd

import scrape, store


def main():
    school_data = pd.DataFrame(None, columns=['# Applicants', '# Faculty'])

    while True:
        soup, name = scrape.find_school_princeton_page(input("Enter school name: "))
        store.store(soup, name, school_data)
        print(school_data, '\n')


main()
