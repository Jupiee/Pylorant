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

        '''

        file: File path of excel sheet

        '''

        self._file= file
        self._db= None
        self._driver= webdriver.Chrome(str(os.getenv("PATH")))

    def openDataBook(self) -> None:

        '''Opens/Creates a text file'''

        self._db= open("databook.txt", "a+")

    def writeData(self, data) -> None:
        
        '''Writes data in the text file'''

        self._db.write(f"username: {data[0]}\ntag: {data[1]}\nregion: {data[2]}\naccount level: {data[3]}\nrank: {data[4]}\n\n")

    def closeDataBook(self) -> None:

        '''Closes the text file'''

        self._db.close()

    def openfile(self) -> None:

        '''Loads the excel file and opens its active sheet and sends the active file to checkData method'''

        efile= load_workbook(self._file).active
        self.checkData(efile)
        
    def openWebsite(self) -> None:

        '''Starts up the Chrome driver with riot site'''

        self._driver.get(str(os.getenv("URL")))
        self._driver.maximize_window()

    def checkData(self, file) -> None:

        '''Opens the text file and iterates over the data in excel file for checking and writing in text file'''

        self.openDataBook()

        for i in file:

            self.sendCreds(i[0].value, i[1].value)
            data= self.retrieveInfo()

            if data != -1:
                self.writeData(data)

        self.closeDataBook()


    def sendCreds(self, username, password) -> None:

        '''Waits for elements to load and sends username and password to login to the website'''

        try:
            usernameelm= WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "username")))
            passelm= WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.NAME, "password")))
            signin_elm= WebDriverWait(self._driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Sign In"]')))

            self._driver.find_element(By.NAME, "username").send_keys(username)
            self._driver.find_element(By.NAME, "password").send_keys(password)
            self._driver.find_element(By.CSS_SELECTOR, 'button[title="Sign In"]').click()

        except:
            
            pass

    def retrieveInfo(self) -> tuple:
        
        '''Waits for elements to load and scrapes in-game name and tag, sends those into riot Api and returns In-game name, Tag, Region, Account level and Rank'''

        try:
            
            riotidelm= WebDriverWait(self._driver, 13).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="riot-id__riotId"]')))
            riottagelm= WebDriverWait(self._driver, 13).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[data-testid="riot-id__tagline"]')))

            ign= self._driver.find_element(By.CSS_SELECTOR, 'input[data-testid="riot-id__riotId"]').get_attribute("value")
            tag= self._driver.find_element(By.CSS_SELECTOR, 'input[data-testid="riot-id__tagline"]').get_attribute("value")

            accinfo= self.__getitem__(ign, tag)
            
            element= self._driver.find_element(By.CSS_SELECTOR, 'div[data-testid="riotbar:account:summonername"]')
            hover = ActionChains(self._driver, duration= 1500).move_to_element(element).perform()


            self._driver.find_element(By.CSS_SELECTOR, 'a[data-testid="riotbar:account:link-logout"]').click()

            return (ign, tag, accinfo[0], accinfo[1], accinfo[2])

        except:

            return -1

    def __getitem__(self, ign, tag) -> tuple:

        '''Sends in-game name and tag into riot Api for Get request and returns Region, Account level and Rank'''

        api1= requests.get(url= f"https://api.henrikdev.xyz/valorant/v1/account/{ign}/{tag}").json()
        api2= requests.get(url= f"https://api.henrikdev.xyz/valorant/v1/mmr-history/{api1['data']['region']}/{ign}/%23{tag}").json()

        region= api1['data']['region']
        acclevel= api1['data']['account_level']
        rank= api2['data'][0]['currenttierpatched']

        return (region, acclevel, rank)
            