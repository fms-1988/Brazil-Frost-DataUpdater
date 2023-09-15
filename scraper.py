import pandas as pd
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import os
import glob
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

#configurate download folder
#file_path = "data/"
file_path = os.path.abspath("data/")
options = Options()
options.add_argument('-headless') # Add this if you don't want the browser GUI to appear in CI environment
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", file_path)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
#options.binary_location = '/usr/bin/firefox'#'/snap/bin/firefox'  # Explicitly specify Firefox binary path

#open webpage
#from selenium.webdriver.firefox.service import Service
#service = Service()
#service.firefox_binary = '/usr/bin/firefox'
#driver = webdriver.Firefox(service=service, options=options)
driver = webdriver.Firefox(options=options)
driver.get('https://portal.inmet.gov.br/paginas/geadas#')
time.sleep(10)

#---------Define_functions------------

def incert_data(date):
    element1 = driver.find_element(By.ID, 'datepicker')
    element1.clear() #exclude original data
    element1.send_keys(date) #put new date


#select the kind of observation (1 = convencional; 2 = automática)
def kind_of_observation(i):
    #element2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[1]/div[1]') #convencional
    element2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[1]/div['+str(i)+']') #automática
    element2.click()
    time.sleep(5)


def search():
    element3 = driver.find_element(By.ID, 'pesquisar')
    element3.click()
    time.sleep(5)

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
def download_():
    try:
        element4 = driver.find_element(By.CLASS_NAME, 'download')
        element4.click()
        time.sleep(5)
    except (NoSuchElementException, ElementNotVisibleException):
        # If the element isn't found or isn't visible, print an error message
        #print(f"No data available to this month")
        raise Exception("No_data_available")


#change the original name of download file to 'temporary_data.csv'
def change_file_name():
    original_file_path = os.path.join(file_path, "Geadas*")
    original_file_path = glob.glob(original_file_path)[0]
    new_file_path = os.path.join(file_path, "new_data.csv")
    os.rename(original_file_path, new_file_path)

#------------execute_functions

#exclude the file that will be replaced
new_data_path = os.path.join(file_path, "new_data.csv")
if os.path.exists(new_data_path):
    os.remove(new_data_path)

#read the database to be updated
data = pd.read_csv(os.path.join(file_path, "data.csv"))

#When was the dast update?
#last_date_str = pd.read_csv(os.path.join(file_path, "last_update.csv")).columns[0]
#last_date = datetime.strptime(last_date_str, '%d/%m/%Y').date()

#new_date
new_date = date.today()
new_date_str = new_date.strftime('%d/%m/%Y')

# incert date on the website
incert_data(new_date_str)

# chose between '1 = convencional' and '2 = automática'
time.sleep(5)
kind_of_observation(1)

#click on 'pesquisar'
search()

#click on 'download' and update data.csv if exist information
try:
    download_()
    change_file_name()
    #read and concatenate files
    new_data = pd.read_csv(os.path.join(file_path, "new_data.csv"), sep=';')
    data = pd.concat([data, new_data], ignore_index=True)
except Exception as e:
    #if str(e) == "No_data_available":
    #    print("No_data_available")
    None

#save data
data.to_csv(os.path.join(file_path, "data.csv"), index=False)

#update the file: last_update.csv
last_date_dir = os.path.join(file_path, "last_update.csv")
with open(last_date_dir, 'w') as file:
    file.write(new_date_str)
