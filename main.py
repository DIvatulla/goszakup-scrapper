import sys
sys.path.append("./modules")
import goszakup
import json
from bs4 import BeautifulSoup

def load_config():
    with open("./config.json", 'r') as file:
        conf = json.load(file)
        
    return(goszakup.goszakup_filters(conf["year"],\
        conf["customer"], conf["spec"], conf["number"], conf["month"],\
        conf["year"], conf["status"], conf["subject_type"]))

gov_buyings_filter = load_config()
gz = goszakup.goszakup(gov_buyings_filter)
goszakup.excel.make_table(gz, "./goszakup_table.xlsx")
