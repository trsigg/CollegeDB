import pandas as pd

import scrape, store


def text_matches(text):
    return lambda tag: tag.string == text


def nth_sibling(tag, num):
    i = 0
    for sibling in tag.next_siblings:
        i += 1
        if i == num:
            return sibling


def main():
    school_data = pd.DataFrame(None, columns=['# Applicants', '# Faculty'])

    while True:
        soup = scrape.find_school_princeton_page(input("Enter school name: "))
        admissions = soup.find(id='admissions')
        print(nth_sibling(soup.find(text_matches('Applicants')), 2).string)
        #  print(admissions.div)
        #  store.store(scrape.find_school_princeton_page(input("Enter school name: ")), school_data)
        #  print(school_data)


main()
