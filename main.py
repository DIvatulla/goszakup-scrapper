#!/usr/bin/python3

import sys
sys.path.append("./modules")
import goszakup
import xmlp
import re
from bs4 import BeautifulSoup

gov_buyings_filter = goszakup.goszakup_filters(customer="Атыра", year="2026")
print(gov_buyings_filter.urlify())


gz = goszakup.goszakup(gov_buyings_filter)
soup = BeautifulSoup(gz.get(), features="lxml")
print(str(soup.find_all('tbody')[1].decode_contents()))


#print(parser.parse())
