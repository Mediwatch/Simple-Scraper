from bs4.element import CData
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from strings import COOKIE

import random
import requests
import json

from time import sleep

from pprint import pprint

cookie = {
    ".AspNetCore.Identity.Application": COOKIE
}

headers={
    "content-type": "application/json; charset=utf-8"
}

prices = [11, 10, 5, 50, 15]
lieux = ["Paris", "Toulouse", "Marseille", "Rouen", "Grenoble", "Reims"]
starts = ["15", "16", "17"]
ends = ["18", "19", "20"]

debuts = ["08", "09", "10"]
fins = ["15", "16", "17"]
quarts = ["00", "15", "30", "45"]

def formation_medicale():
    CREDITS = "Ma formation médicale"

    URL = "https://www.maformationmedicale.fr/recherche"

    driver = webdriver.Firefox()

    driver.get(URL)

    all_formations = []

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
        try:
            a = driver.find_element_by_xpath(f"//a[@aria-label='Go to page number {idx + 1}']")
            a.find_element_by_xpath("./..").click()
        except: pass

    driver.close()


    for formation in all_formations:
        r = requests.post("https://beta.mediwatch.fr/Formation", verify=False, data=json.dumps(formation), cookies=cookie, headers=headers)
        print(r)
        #exit(1)

def chem_sante():
    CREDITS = "Collège des Hautes Etudes en Médecine"

    URL = "https://www.chem-sante.fr/formations/"

    driver = webdriver.Firefox()

    driver.get(URL)

    all_formations = []

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elems = driver.page_source
        soup = BeautifulSoup(elems, 'lxml')

        all_formations_in_one_page = soup.find_all('a', class_='formation-preview')
        for formation in all_formations_in_one_page:
            data = {
                "name": formation.find('div', class_='preview-content').find('div', class_='preview-title').string,
                "description": "Aucune description n'a été proposée par le formateur.",
                "former": CREDITS,
                "target": str(formation.find('div', class_='preview-content').find('div', class_='preview-info').findAll('p', class_='preview-info-group')[1]).split('</strong>')[-1][:-4].strip(),
                "organizationName": CREDITS,
                "location": str(formation.find('footer', class_='preview-footer').find('span', class_='presentiel').string).strip(),
                "price": random.choice(prices),
                "startDate": "2021-10-" + random.choice(starts) + "T" + random.choice(debuts) + ":" + random.choice(quarts) + ":00+02:00",
                "endDate": "2021-10-" + random.choice(ends) + "T" + random.choice(fins) + ":" + random.choice(quarts) + ":00+02:00",
                "id": "00000000-0000-0000-0000-000000000000",
                "articleID":"NO_ID",
                "quantityCurrent":0,
                "quantityMax":0,
                "contact": "0123456789"
            }
            r = requests.post("https://beta.mediwatch.fr/Formation", verify=False, data=json.dumps(data), cookies=cookie, headers=headers)
            print(r)
        break

    driver.close()

chem_sante()