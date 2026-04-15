#!/usr/bin/python3
import pdb
import sys
sys.path.append("./modules")
import goszakup
import xmlp
import re
from bs4 import BeautifulSoup

gov_buyings_filter = goszakup.goszakup_filters(customer="Атыра", year="2026", count_record=2000)
gz = goszakup.goszakup(gov_buyings_filter)
goszakup.excel.make_table(gz, "./goszakup_table.xlsx")