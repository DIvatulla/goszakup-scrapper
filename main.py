import sys
sys.path.append("./modules")
import goszakup

gov_buyings_filter = goszakup.goszakup_filters()
print(gov_buyings_filter.urlify())

gz = goszakup.goszakup(gov_buyings_filter)
print(gz.data.body)
