#!/usr/bin/python3

import sys
sys.path.append("./modules")
import goszakup
import xmlm

gov_buyings_filter = goszakup.goszakup_filters(name="Атыра", year="2026")
print(gov_buyings_filter.urlify())

gz = goszakup.goszakup(gov_buyings_filter)
print(gz.data.body)

#for line in gz.data.body.split('\n'):
