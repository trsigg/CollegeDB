import scrape


def clean_int(str):
    return int(str.replace(',', ''))


def store(soup, name, df):
    data = []
    data.append(clean_int(scrape.get_tag_after(soup, 'Applicants').string))   # Applicants
    data.append(clean_int(scrape.get_tag_after(soup, 'Total Faculty').string))  # Faculty
    df.loc[name] = data
