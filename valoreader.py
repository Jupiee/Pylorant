import os, requests
from openpyxl import load_workbook
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

load_dotenv()

class Valoreader:

    def __init__(self, file):

        self._file= file
        self._db= None
        self._driver= webdriver.Chrome(str(os.getenv("PATH")))

    def openDataBook(self):

        self._db= open("databook.txt", "a+")

    def writeData(self, data):
        
        self._db.write(f"username: {data[0]}\ntag: {data[1]}\nregion: {data[2]}\naccount level: {data[3]}\nrank: {data[4]}\n\n")

    def closeDataBook(self):

        self._db.close()

    def openfile(self):

        efile= load_workbook(self._file).active
        print(efile)
        self.checkData(efile)
        
    def openWebsite(self):

        self._driver.get(str(os.getenv("URL")))

    def checkData(self, file):

        self.openDataBook()

        for i in file:

            self.sendCreds(i[0].value, i[1].value)
            data= self.retrieveInfo()

            if data != "wrong credentials or Api is currently down":
                self.writeData(data)

        self.closeDataBook()


    def sendCreds(self, username, password):
        
        try:
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "username")))
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "password")))
            WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Sign In"]')))

            self._driver.find_element(By.NAME, "username").send_keys(username)
            self._driver.find_element(By.NAME, "password").send_keys(password)
            self._driver.find_element(By.CSS_SELECTOR, 'button[title="Sign In"]').click()

        except:
            
            pass

    def retrieveInfo(self):
        
        try:
            
            WebDriverWait(self._driver, 13).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="riot-id__riotId"]')))
            WebDriverWait(self._driver, 13).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="riot-id__tagline"]')))

            ign= self._driver.find_element(By.CSS_SELECTOR, 'input[data-testid="riot-id__riotId"]').get_attribute("value")
            tag= self._driver.find_element(By.CSS_SELECTOR, 'input[data-testid="riot-id__tagline"]').get_attribute("value")

            accinfo= self.__getitem__(ign, tag)
            
            element= self._driver.find_element(By.CSS_SELECTOR, 'div[data-testid="riotbar:account:summonername"]')
            hover = ActionChains(self._driver, duration= 1500).move_to_element(element).perform()


            self._driver.find_element(By.CSS_SELECTOR, 'a[data-testid="riotbar:account:link-logout"]').click()

            return (ign, tag, accinfo[0], accinfo[1], accinfo[2])

        except:

            return "wrong credentials or Api is currently down"

    def __getitem__(self, ign, tag):

        api1= requests.get(url= f"https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}").json()
        api2= requests.get(url= f"https://api.henrikdev.xyz/valorant/v1/mmr-history/{api1['data']['region']}/{ign}/%23{tag}").json()

        region= api1['data']['region']
        acclevel= api1['data']['account_level']
        rank= api2['data'][0]['currenttierpatched']

        return (region, acclevel, rank)
            