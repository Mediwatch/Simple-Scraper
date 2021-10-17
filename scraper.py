from bs4.element import CData
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from pprint import pprint

# TODO: Améliorer en allant chercher les informations dans la page de la formation elle-même

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
            all_formations.append({
                "Name": formation.find('h3').string,
                "Description": formation.find('div', class_='item-resume').string,
                "Former": CREDITS,
                "Target": formation.find('div', class_='item-professions').find('div', class_='value').find('ul').find('li').string,
                "OrganizationName": CREDITS,
                "Location": "LOCALISATION A CHERCHER DANS LA PAGE DE LA FORMATION",
                "Price": "PRIX A CHERCHER DANS LA PAGE DE LA FORMATION",
                "StartDate": "DATE DE DEBUT A CHERCHER DANS LA PAGE DE LA FORMATION",
                "EndDate": "DATE DE FIN A CHERCHER DANS LA PAGE DE LA FORMATION",
            })
        except: pass

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    a = driver.find_element_by_xpath(f"//a[@aria-label='Go to page number {idx}']")
    a.find_element_by_xpath("./..").click()

driver.close()

pprint(all_formations)