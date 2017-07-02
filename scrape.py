from bs4 import BeautifulSoup
from urllib.request import urlopen, quote


def get_soup(url):
    #  print(url)
    return BeautifulSoup(urlopen(url), 'lxml')


def find_school_princeton_page(name):
    search_soup = get_soup('https://www.princetonreview.com/college-search?search=' + quote(name))
    poss_heading = search_soup.find('h2', class_='margin-top-none')
    while True:
        poss_link = poss_heading.a
        poss_name = poss_link.string
        if input("Is %s the school you are looking for? " % poss_name) == 'y':
            return get_soup('https://www.princetonreview.com' + poss_link['href']), poss_name
        poss_heading = poss_heading.find_next('h2', class_='margin-top-none')


def text_matches(text):
    return lambda tag: tag.string == text


def nth_sibling(tag, num):
    i = 0
    for sibling in tag.next_siblings:
        i += 1
        if i == num:
            return sibling


def get_tag_after(soup, text):
    match = soup.find(text_matches(text))

    if match:
        return nth_sibling(match, 2)

    return None
