# Some Notes:
# Pyrebase needs to be imported for the automatic script to be able to do its thing.
# Without pyrebase the script needs to be modified to output a JSON file which can then be manually uploaded to
# firebase. This is cumbersome so please install the pyrebase library to run this.
# This can be done using pip. On ubuntu run: sudo apt-get install python3-pip. Pyrebase is not compatible with any
# versions of python 2 so python 3 is required and I have only been able to make it work with Python 3.5. As such
# my recommendation is that you work with that interpreter.

import requests
import pyrebase
from bs4 import BeautifulSoup
import time
from datetime import datetime

config = {
    "apiKey": "AIzaSyAXURMO3ANz5mPSytykWLpZTJ0oGWmgoXI",
    "authDomain": "world-health-org-vacc-details",
    "databaseURL": "https://world-health-org-vacc-details.firebaseio.com/",
    "storageBucket": "world-health-org-vacc-details.appspot.com"
}

# First page of the website we want to get information from.
url_to_scrape = 'http://apps.who.int/immunization_monitoring/globalsummary/schedules'

r = requests.get(url_to_scrape)

# The BeautfulSoup library does some magic.
soup = BeautifulSoup(r.text, "lxml")

# This is our countries code extracted from the first page. It lists all countries in the form: 'AUS' as an example.
# We use this in combination with the url below to iterate through all the countries for all their vaccine schedules.
countries_codes = []

# This is the final dictionary that is pushed to firebase. The format is as follows:
# {Country: {Vaccine: [vaccine information], ...}, ... }
vaccinesByCountry = {}

# So I didn't want the database to be sorted by country code, such as 'AUS', as some we confusing and non intuitive.
# As such I created a dictionary of the "Country Code: Full Country Name" format. So for example Australia would be
# represented as: {'AUS' : 'Australia'}
# This was also obtained from the first page.
countryKeyValuePairs = {}

# This is where the countries_codes and countryKeyValuePairs list and dictionary is populated. The find method is used
# to get all rows in the html document that have the <select></select> tag and of those we only choose the ones with
# the attribute 'name' = 'sc[c][]'. These rows are the ones with the country codes that we want. All the tag knowledge
# comes from checking out the html Source files.
for table_row in soup.find("select", attrs={"name": "sc[c][]"}):
    if table_row != '\n':
        print(table_row.attrs['value'])
        countries_codes.append(table_row.attrs['value'])
        countryKeyValuePairs[table_row.attrs['value']] = table_row.text.strip()

# Above we got all the unique country codes and placed them into the countries_codes list. Here we iterate through that
# list and interpolate the code into the URL at the obvious place. This url was obtained by selecting ALL the vaccines
# for a particular country.
for code in countries_codes:
    url_to_scrape = 'http://apps.who.int/immunization_monitoring/globalsummary/schedules?sc%5Bc%5D%5B%5D=' + code + '&sc%5Bd%5D=&sc%5Bv%5D%5B%5D=AP&sc%5Bv%5D%5B%5D=BCG&sc%5Bv%5D%5B%5D=CHOLERA&sc%5Bv%5D%5B%5D=DIP&sc%5Bv%5D%5B%5D=DIPHTERIA&sc%5Bv%5D%5B%5D=DT&sc%5Bv%5D%5B%5D=DTAP&sc%5Bv%5D%5B%5D=DTAPHEP&sc%5Bv%5D%5B%5D=DTAPHEPBIPV&sc%5Bv%5D%5B%5D=DTAPHEPIPV&sc%5Bv%5D%5B%5D=DTAPHIB&sc%5Bv%5D%5B%5D=DTAPHIBHEPB&sc%5Bv%5D%5B%5D=DTAPHIBHEPIPV&sc%5Bv%5D%5B%5D=DTAPHIBIPV&sc%5Bv%5D%5B%5D=DTAPIPV&sc%5Bv%5D%5B%5D=DTIPV&sc%5Bv%5D%5B%5D=DTPHIBHEP&sc%5Bv%5D%5B%5D=DTWP&sc%5Bv%5D%5B%5D=DTWPHEP&sc%5Bv%5D%5B%5D=DTWPHIB&sc%5Bv%5D%5B%5D=DTWPHIBHEPB&sc%5Bv%5D%5B%5D=DTWPHIBHEPBIPV&sc%5Bv%5D%5B%5D=DTWPHIBIPV&sc%5Bv%5D%5B%5D=DTWPIPV&sc%5Bv%5D%5B%5D=HEPA&sc%5Bv%5D%5B%5D=HEPA_ADULT&sc%5Bv%5D%5B%5D=HEPAHEPB&sc%5Bv%5D%5B%5D=HEPA_PEDIATRIC&sc%5Bv%5D%5B%5D=HEPB&sc%5Bv%5D%5B%5D=HEPB_ADULT&sc%5Bv%5D%5B%5D=HEPB_PEDIATRIC&sc%5Bv%5D%5B%5D=HEPB_PEDIATRIC&sc%5Bv%5D%5B%5D=HFRS&sc%5Bv%5D%5B%5D=HIB&sc%5Bv%5D%5B%5D=HIB&sc%5Bv%5D%5B%5D=HIBMENC&sc%5Bv%5D%5B%5D=HPV&sc%5Bv%5D%5B%5D=INFLUENZA&sc%5Bv%5D%5B%5D=INFLUENZA_ADULT&sc%5Bv%5D%5B%5D=INFLUENZA_PEDIATRIC&sc%5Bv%5D%5B%5D=IPV&sc%5Bv%5D%5B%5D=JAPENC&sc%5Bv%5D%5B%5D=JE_INACTD&sc%5Bv%5D%5B%5D=JE_LIVEATD&sc%5Bv%5D%5B%5D=MEASLES&sc%5Bv%5D%5B%5D=MENA&sc%5Bv%5D%5B%5D=MENAC&sc%5Bv%5D%5B%5D=MENACWY&sc%5Bv%5D%5B%5D=MENACWY-135+CONJ&sc%5Bv%5D%5B%5D=MENACWY-135+PS&sc%5Bv%5D%5B%5D=MENB&sc%5Bv%5D%5B%5D=MENBC&sc%5Bv%5D%5B%5D=MENC_CONJ&sc%5Bv%5D%5B%5D=MM&sc%5Bv%5D%5B%5D=MMR&sc%5Bv%5D%5B%5D=MMRV&sc%5Bv%5D%5B%5D=MR&sc%5Bv%5D%5B%5D=MUMPS&sc%5Bv%5D%5B%5D=OPV&sc%5Bv%5D%5B%5D=PNEUMO_CONJ&sc%5Bv%5D%5B%5D=PNEUMO_PS&sc%5Bv%5D%5B%5D=RABIES&sc%5Bv%5D%5B%5D=ROTAVIRUS&sc%5Bv%5D%5B%5D=RUBELLA&sc%5Bv%5D%5B%5D=TBE&sc%5Bv%5D%5B%5D=TD&sc%5Bv%5D%5B%5D=TDAP&sc%5Bv%5D%5B%5D=TDAP&sc%5Bv%5D%5B%5D=TDAPIPV&sc%5Bv%5D%5B%5D=TDIPV&sc%5Bv%5D%5B%5D=TT&sc%5Bv%5D%5B%5D=TYPHOID&sc%5Bv%5D%5B%5D=TYPHOIDHEPA&sc%5Bv%5D%5B%5D=VARICELLA&sc%5Bv%5D%5B%5D=VITA&sc%5Bv%5D%5B%5D=VITAMINA&sc%5Bv%5D%5B%5D=YF&sc%5Bv%5D%5B%5D=ZOSTER&sc%5BOK%5D=OK'
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.text, "lxml")

    # This is a list of our vaccine details.
    vaccine_details = []
    # This is a list of vaccines. So for example, {'HepA': [details of Hepa]}
    vaccines = {}

    # All the processing of the vaccine rows happens here. Some trouble was had selecting both odd and even table
    # classes so it was separated into one for loop for odds and one for loops for evens. The information at each
    # column is extracted using table_cells[i].text.strip(). These details were then appended to vaccine details.
    # The id of each vaccine (antigen) was then used to build the vaccines dictionary. This is the line:
    # vaccines[table_cells[1].text.strip()] = vaccine_details.
    # vaccine_details is then redefined so that it is empty and the process repeats.
    # One second is added between each request as a courtesy to the world health organisation website. I was told by
    # the tutorials that this is the polite thing to do. Not that WHO should have any trouble dealing with all the
    # requests that I can make.
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

    # Finally the VaccinesByCountry  dictionary is built using the 'code' variable that we use to iterate through
    # each country. But because we want the format to be 'Australia': Vaccines rather than 'AUS' : Vaccines, the
    # countryKeyValuePairs list is used to get the relevant name of countries based on their code.
    vaccinesByCountry[countryKeyValuePairs[code]] = vaccines
    vaccinesByCountry['DateUpdated'] = datetime.now().strftime('%A %d %B %Y')


# Pyrebase library is used to push the information to firebase.
firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.push(vaccinesByCountry)