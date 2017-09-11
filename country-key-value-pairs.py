import requests
from bs4 import BeautifulSoup
import time


url_to_scrape = 'http://apps.who.int/immunization_monitoring/globalsummary/schedules'

r = requests.get(url_to_scrape)

soup = BeautifulSoup(r.text, "lxml")

# print(soup)

countries_codes = {}
vaccinesByCountry = {}

for table_row in soup.find("select", attrs={"name": "sc[c][]"}):
    if table_row != '\n':
        print(table_row)
        print(table_row.text.strip())
        countries_codes[table_row.attrs['value']] = table_row.text.strip()


# for table_row in soup.find("select", attrs={"name": "sc[c][]"}):
#     print(table_row)
#     if table_row != '\n':
#         print(table_row.attrs['value'])
#         countries_codes.append(table_row.attrs['value'])
#
#     # table_cells = table_row.findAll(name="sc[c][]")
#     # print(table_cells)
#     # time.sleep(1)

print(countries_codes)