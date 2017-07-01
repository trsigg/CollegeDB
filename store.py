import pandas as pd
from bs4 import BeautifulSoup


def store(soup, df):
    attrs = []
    admissions = soup.find(id='admissions')
    academics = soup.find(id='admissions')
