from bs4.element import CData
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from strings import COOKIE

import random
import requests
import json

from pprint import pprint

cookie = {
    ".AspNetCore.Identity.Application": COOKIE
}

headers={
    "content-type": "application/json; charset=utf-8"
}

CREDITS = "Ma formation médicale"

URL = "https://www.maformationmedicale.fr/recherche"

driver = webdriver.Firefox()

driver.get(URL)

all_formations = []

prices = [11, 10, 5, 50, 15]
lieux = ["Paris", "Toulouse", "Marseille", "Rouen", "Grenoble", "Reims"]
starts = ["15", "16", "17"]
ends = ["18", "19", "20"]

debuts = ["08", "09", "10"]
fins = ["15", "16", "17"]
quarts = ["00", "15", "30", "45"]

for idx in range(1, 30):
    driver.execute_script("window.scrollTo(0, 0);")

    elems = driver.page_source
    soup = BeautifulSoup(elems, 'lxml')

    all_formations_in_one_page = soup.find_all('div', class_='search-item')


    for formation in all_formations_in_one_page:
        try:
            desc = formation.find('div', class_='item-resume').string
            all_formations.append({
                "name": formation.find('h3').string,
                "description": "Aucune description n'a été proposée par le formateur." if desc is None else desc,
                "former": CREDITS,
                "target": formation.find('div', class_='item-professions').find('div', class_='value').find('ul').find('li').string,
                "organizationName": CREDITS,
                "location": random.choice(lieux),
                "price": random.choice(prices),
                "startDate": "2021-10-" + random.choice(starts) + "T" + random.choice(debuts) + ":" + random.choice(quarts) + ":00+02:00",
                "endDate": "2021-10-" + random.choice(ends) + "T" + random.choice(fins) + ":" + random.choice(quarts) + ":00+02:00",
                "id": "00000000-0000-0000-0000-000000000000",
                "articleID":"NO_ID",
                "quantityCurrent":0,
                "quantityMax":0,
                "contact": "0123456789"
            })
        except: pass

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    a = driver.find_element_by_xpath(f"//a[@aria-label='Go to page number {idx}']")
    a.find_element_by_xpath("./..").click()

driver.close()


for formation in all_formations:
    requests.post("https://beta.mediwatch.fr/Formation", verify=False, data=json.dumps(formation), cookies=cookie, headers=headers)
