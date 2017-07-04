''' Applicants
Average HS GPA
Total Faculty
with Terminal Degree
Tuition (Out-of-State)
Required Fees
Average Cost for Books and Supplies
On-Campus Room and Board
Comprehensive Fee
Student/Faculty
Most frequent class size

Most frequent lab / sub section size

Admissions selectivity rating
Professors interesting rating
Professors accessible rating
Academic rating
Financial Aid Rating
Quality of life rating
Fire safety rating
Green rating
Return on Investment (ROI) rating
Acceptance Rate
Graduate in 4 years
Graduate in 5 years
Graduate in 6 years
Undergrads living on campus
First-Year Students living on campus
Undergraduates who have borrowed
{GPA Breakdown} '''

import scrape as sc
import store as st
from bs4 import BeautifulSoup
import re
import numpy as np
from urllib.request import urlopen, quote
import pandas as pd


soup = sc.get_soup('https://www.princetonreview.com/schools/1023092/college/university-michigan--ann-arbor')
