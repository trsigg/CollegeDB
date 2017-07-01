from bs4 import BeautifulSoup
from urllib.request import urlopen, quote


def get_soup(url):
    print(url)
    return BeautifulSoup(urlopen(url), 'lxml')


def find_school_princeton_page(name):
    search_soup = get_soup('https://www.princetonreview.com/college-search?search=' + quote(name))
    poss_heading = search_soup.find('h2', class_='margin-top-none')
    while True:
        poss_link = poss_heading.a
        poss_name = poss_link.string
        if input("Is %s the school you are looking for?" % poss_name) == 'y':
            return get_soup('https://www.princetonreview.com' + poss_link['href'])
        poss_heading = poss_heading.find_next('h2', class_='margin-top-none')
