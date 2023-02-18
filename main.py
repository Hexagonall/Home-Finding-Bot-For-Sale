import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

Url = "https://www.sahibinden.com/satilik-villa/istanbul-sariyer"
Google_forms = "https://docs.google.com/forms/d/e/1FAIpQLSfwkItuOkqEyAMtSuJm33dG2-YkyvgSfCZwW30nrhE3ayV5Ag/viewform?usp=sf_link"
chromedriver = os.environ.get("driver")
header = {
    "User-Agent": os.environ.get("UserAgent"),
    "Accept-Language": "en-GB,en;q=0.9,tr-TR;q=0.8,tr;q=0.7,en-US;q=0.6",
}

class DataEntryJobAutomation:
    def __init__(self,service):
        self.driver = webdriver.Chrome(service=Service(service))
        self.name_list = []
        self.price_list = []
        self.link_list = []
        self.questions = []

    def get_data(self, sahibinden_url):
        response = requests.get(sahibinden_url, headers=header)
        response.raise_for_status()
        data = response.text

        self.soup = BeautifulSoup(data, "html.parser")

        titles = self.soup.find_all(name="a", class_="classifiedTitle" )
        self.name_list = [title.getText().strip() for title in titles]

        links = self.soup.find_all(name="a", class_="classifiedTitle" )
        self.link_list = [f"https://www.sahibinden.com{link['href']}"for link in links]

        prices = self.soup.select(".searchResultsPriceValue div")
        self.price_list = [price.getText().strip() for price in prices]


    def store_data(self,form):

        for i in range(0,len(self.name_list)):

            self.driver.get(form)
            time.sleep(1)

            questions = self.driver.find_elements(By.CSS_SELECTOR, ".Xb9hP input")

            self.questions = [q for q in questions]

            questions1 = self.questions[0]
            questions2 = self.questions[1]
            questions3 = self.questions[2]
            questions1.send_keys(self.name_list[i])

            questions2.send_keys(self.link_list[i])

            questions3.send_keys(self.price_list[i])

            button = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            button.click()
            time.sleep(1)

            self.driver.find_element(By.CSS_SELECTOR, ".c2gzEf a").click()
            time.sleep(3)

result = DataEntryJobAutomation(chromedriver)
result.get_data(Url)
result.store_data(Google_forms)