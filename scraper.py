#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import os
import glob
import time

#driver=webdriver.Firefox()


# In[6]:


#configurate download folder
from selenium.webdriver.firefox.options import Options

download_dir = "/home/felipe/Documents/comp/inmet_actions"

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", download_dir)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")


# In[7]:


#open webpage
driver = webdriver.Firefox(options=options)
driver.get('https://portal.inmet.gov.br/paginas/geadas#')


# In[8]:


def incert_data(date):
    element1 = driver.find_element(By.ID, 'datepicker')
    element1.clear() #exclude original data
    element1.send_keys(date) #put new date


# In[27]:


#select the kind of observation (1 = convencional; 2 = automática)
def kind_of_observation(i):
    #element2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[1]/div[1]') #convencional
    element2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/div[1]/div['+str(i)+']') #automática
    element2.click()
    time.sleep(1.5)


# In[10]:


def search():
    element3 = driver.find_element(By.ID, 'pesquisar')
    element3.click()


# In[11]:


from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

def download_():
    try:
        element4 = driver.find_element(By.CLASS_NAME, 'download')
        element4.click()
        time.sleep(3)
    except (NoSuchElementException, ElementNotVisibleException):
        # If the element isn't found or isn't visible, print an error message
        #print(f"No data available to this month")
        raise Exception("No_data_available")


# In[12]:


#change the original name of download file to 'temporary_data.csv'
def change_file_name():
    original_file_path = os.path.join(download_dir, "Geadas*")
    original_file_path = glob.glob(original_file_path)[0]
    new_file_path = os.path.join(download_dir, "new_data.csv")
    os.rename(original_file_path, new_file_path)

            


# In[29]:


from datetime import datetime
from dateutil.relativedelta import relativedelta

new_data_path = os.path.join(download_dir, "new_data.csv")
if os.path.exists(new_data_path):
    os.remove(new_data_path)

data = pd.DataFrame()
initial_date_str = '01/08/2003'
for i in range(250):
    print(i)
    # Initial date
    initial_date = datetime.strptime(initial_date_str, '%d/%m/%Y').date()
    # Add one month
    new_date = initial_date + relativedelta(months=i)
    new_date_str = new_date.strftime('%d/%m/%Y')
    # incert date on the website
    incert_data(new_date_str)
    # chose between '1 = convencional' and '2 = automática'
    kind_of_observation(1)
    #click on 'pesquisar'
    search()
    #click on 'download'
    #download_()
    try:
        download_()
        change_file_name()
        #read and concatenate files
        new_data = pd.read_csv(os.path.join(download_dir, "new_data.csv"), sep=';')
        data = pd.concat([data, new_data], ignore_index=True)
    except Exception as e:
        #if str(e) == "No_data_available":
        #    print("No_data_available")
        None


    


# In[32]:


data.to_csv(os.path.join(download_dir, "data.csv"), index=False)


# In[20]:


last_update_dir = os.path.join(download_dir, "last_update.csv")
with open(last_update_dir, 'w') as file:
    file.write(initial_date_str)


# In[26]:


pd.read_csv(os.path.join(download_dir, "last_update.csv")).columns[0]


# In[95]:


for i in range(240):
    # Initial date
    initial_date = datetime.strptime(initial_date_str, '%d/%m/%Y').date()
    # Add one month
    new_date = initial_date + relativedelta(months=i)
    new_date_str = new_date.strftime('%d/%m/%Y')
    print(new_date_str)


# In[ ]:




