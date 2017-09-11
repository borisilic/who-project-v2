import requests
import pyrebase

config = {
    "apiKey": "AIzaSyAXURMO3ANz5mPSytykWLpZTJ0oGWmgoXI",
    "authDomain": "world-health-org-vacc-details",
    "databaseURL": "https://world-health-org-vacc-details.firebaseio.com/",
    "storageBucket": "world-health-org-vacc-details.appspot.com"
}

# So it works for now. To expand we can scrape the country codes from the initial selections page
# and substitute them into the url. That way with a single run of the script we can get the information
# for all the countries that World Health Org lists and upload that info into the db. The difficulty
# will lie in creating the proper for loop to organise the dictionary, but it shouldn't be too difficult.
# To run this we I used the python 3.5 interpreter rather than the anaconda 3.6 one. For some reason
# anaconda would refuse to find the pyrebase library. Pyrebase has to be installed with pip. Ensure
# that pip3 is used for python 3 rather than pip itself as that usually defaults to python 2.x.

from bs4 import BeautifulSoup
import time

url_to_scrape = 'http://apps.who.int/immunization_monitoring/globalsummary/schedules?sc%5Bc%5D%5B%5D=AUS&sc%5Bd%5D=&sc%5Bv%5D%5B%5D=AP&sc%5Bv%5D%5B%5D=BCG&sc%5Bv%5D%5B%5D=CHOLERA&sc%5Bv%5D%5B%5D=DIP&sc%5Bv%5D%5B%5D=DIPHTERIA&sc%5Bv%5D%5B%5D=DT&sc%5Bv%5D%5B%5D=DTAP&sc%5Bv%5D%5B%5D=DTAPHEP&sc%5Bv%5D%5B%5D=DTAPHEPBIPV&sc%5Bv%5D%5B%5D=DTAPHEPIPV&sc%5Bv%5D%5B%5D=DTAPHIB&sc%5Bv%5D%5B%5D=DTAPHIBHEPB&sc%5Bv%5D%5B%5D=DTAPHIBHEPIPV&sc%5Bv%5D%5B%5D=DTAPHIBIPV&sc%5Bv%5D%5B%5D=DTAPIPV&sc%5Bv%5D%5B%5D=DTIPV&sc%5Bv%5D%5B%5D=DTPHIBHEP&sc%5Bv%5D%5B%5D=DTWP&sc%5Bv%5D%5B%5D=DTWPHEP&sc%5Bv%5D%5B%5D=DTWPHIB&sc%5Bv%5D%5B%5D=DTWPHIBHEPB&sc%5Bv%5D%5B%5D=DTWPHIBHEPBIPV&sc%5Bv%5D%5B%5D=DTWPHIBIPV&sc%5Bv%5D%5B%5D=DTWPIPV&sc%5Bv%5D%5B%5D=HEPA&sc%5Bv%5D%5B%5D=HEPA_ADULT&sc%5Bv%5D%5B%5D=HEPAHEPB&sc%5Bv%5D%5B%5D=HEPA_PEDIATRIC&sc%5Bv%5D%5B%5D=HEPB&sc%5Bv%5D%5B%5D=HEPB_ADULT&sc%5Bv%5D%5B%5D=HEPB_PEDIATRIC&sc%5Bv%5D%5B%5D=HEPB_PEDIATRIC&sc%5Bv%5D%5B%5D=HFRS&sc%5Bv%5D%5B%5D=HIB&sc%5Bv%5D%5B%5D=HIB&sc%5Bv%5D%5B%5D=HIBMENC&sc%5Bv%5D%5B%5D=HPV&sc%5Bv%5D%5B%5D=INFLUENZA&sc%5Bv%5D%5B%5D=INFLUENZA_ADULT&sc%5Bv%5D%5B%5D=INFLUENZA_PEDIATRIC&sc%5Bv%5D%5B%5D=IPV&sc%5Bv%5D%5B%5D=JAPENC&sc%5Bv%5D%5B%5D=JE_INACTD&sc%5Bv%5D%5B%5D=JE_LIVEATD&sc%5Bv%5D%5B%5D=MEASLES&sc%5Bv%5D%5B%5D=MENA&sc%5Bv%5D%5B%5D=MENAC&sc%5Bv%5D%5B%5D=MENACWY&sc%5Bv%5D%5B%5D=MENACWY-135+CONJ&sc%5Bv%5D%5B%5D=MENACWY-135+PS&sc%5Bv%5D%5B%5D=MENB&sc%5Bv%5D%5B%5D=MENBC&sc%5Bv%5D%5B%5D=MENC_CONJ&sc%5Bv%5D%5B%5D=MM&sc%5Bv%5D%5B%5D=MMR&sc%5Bv%5D%5B%5D=MMRV&sc%5Bv%5D%5B%5D=MR&sc%5Bv%5D%5B%5D=MUMPS&sc%5Bv%5D%5B%5D=OPV&sc%5Bv%5D%5B%5D=PNEUMO_CONJ&sc%5Bv%5D%5B%5D=PNEUMO_PS&sc%5Bv%5D%5B%5D=RABIES&sc%5Bv%5D%5B%5D=ROTAVIRUS&sc%5Bv%5D%5B%5D=RUBELLA&sc%5Bv%5D%5B%5D=TBE&sc%5Bv%5D%5B%5D=TD&sc%5Bv%5D%5B%5D=TDAP&sc%5Bv%5D%5B%5D=TDAP&sc%5Bv%5D%5B%5D=TDAPIPV&sc%5Bv%5D%5B%5D=TDIPV&sc%5Bv%5D%5B%5D=TT&sc%5Bv%5D%5B%5D=TYPHOID&sc%5Bv%5D%5B%5D=TYPHOIDHEPA&sc%5Bv%5D%5B%5D=VARICELLA&sc%5Bv%5D%5B%5D=VITA&sc%5Bv%5D%5B%5D=VITAMINA&sc%5Bv%5D%5B%5D=YF&sc%5Bv%5D%5B%5D=ZOSTER&sc%5BOK%5D=OK'

r = requests.get(url_to_scrape)
soup = BeautifulSoup(r.text, "lxml")

vaccine_details = []
vaccines = {}
countries = {}

while True:
    for table_row in soup.select('table .even'):
        table_cells = table_row.findAll('td')
        for i in range(2, 6):
            vaccine_details.append(table_cells[i].text.strip())
        vaccines[table_cells[1].text.strip()] = vaccine_details
        vaccine_details = []
        time.sleep(1)

    for table_row in soup.select('table .odd'):
        table_cells = table_row.findAll('td')
        for i in range(2, 6):
            vaccine_details.append(table_cells[i].text.strip())
        vaccines[table_cells[1].text.strip()] = vaccine_details
        vaccine_details = []
        time.sleep(1)

    break

for k, v in vaccines.items():
    print(k, v)

countries['Australia'] = vaccines
countries['China'] = vaccines

firebase = pyrebase.initialize_app(config)

db = firebase.database()

db.child("countries").push(countries)


