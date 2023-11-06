import csv
import os
import numpy as np
###############################
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
######Declaring Web Driver#####
driver = webdriver.Chrome()
######CONSTANTS#####
FOLDER_NAME = 'Monthly-Basis-Data'
CITY = 'Khairpur,'
CITY_LINKNAME = '@1384078' #If with name then mention pakistan before, i.e. pakistan/lahore
YEAR_LOWER_LIMIT = 2012
YEAR_UPPER_LIMIT = 2023
######File System#####
try:
    os.mkdir(FOLDER_NAME)
except:
    print(FOLDER_NAME + " already exists")

#####
file_name = CITY.capitalize() +" Monthly Basis Data " + str(YEAR_LOWER_LIMIT) + "-" + str(YEAR_UPPER_LIMIT)+".csv"
file_path = FOLDER_NAME+"/"+file_name
file = open(file_path, 'w', newline='')
writer = csv.writer(file)
writer.writerow(["Month","Year","City","Low Temperature","Average Temperature","High Temperature","Low Humidity","Avg Humidity","High Humidity","Low Pressurre","Avg Pressure","High Pressure"])

    
def getInformation():
    table = driver.find_element(By.XPATH , '/html/body/div[5]/main/article/div[5]/div[1]/table')
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    trList = tbody.find_elements(By.TAG_NAME, 'tr')
    ####HIGH ROW trList[0]###
    highTemp = trList[0].find_elements(By.TAG_NAME, 'td')[0].text.split('C')[0]+'C'
    highHumidity = trList[0].find_elements(By.TAG_NAME, 'td')[1].text.split('%')[0]+'%'
    highPressure = trList[0].find_elements(By.TAG_NAME, 'td')[2].text.split('mbar')[0]+'mbar'
    ####LOW ROW trList[1]###
    lowTemp = trList[1].find_elements(By.TAG_NAME, 'td')[0].text.split('C')[0]+'C'
    lowHumidity = trList[1].find_elements(By.TAG_NAME, 'td')[1].text.split('%')[0]+'%'
    lowPressure = trList[1].find_elements(By.TAG_NAME, 'td')[2].text.split('mbar')[0]+'mbar'
    ####Average ROW trList[1]###
    avgTemp = trList[2].find_elements(By.TAG_NAME, 'td')[0].text.split('C')[0]+'C'
    avgHumidity = trList[2].find_elements(By.TAG_NAME, 'td')[1].text.split('%')[0]+'%'
    avgPressure = trList[2].find_elements(By.TAG_NAME, 'td')[2].text.split('mbar')[0]+'mbar'

    return [lowTemp, avgTemp, highTemp, lowHumidity, avgHumidity, highHumidity, lowPressure, avgPressure, highPressure]

# navigate to the website you want to scrape
for year in range(YEAR_LOWER_LIMIT, YEAR_UPPER_LIMIT+1):
    for month in range (1, 13):
        if(year >= 2023 and month >= 3):
            break;
        try:
            driver.get("https://www.timeanddate.com/weather/"+CITY_LINKNAME+"/historic?month="+str(month)+"&year="+str(year))
            cityData = [month, year, CITY.capitalize()]
            monthSummary = getInformation()
            row = np.concatenate((cityData, monthSummary))
            writer.writerow(row)
        except:
            print("Error While Fetching " + str(month) + "-" + str(year))

# close the browser


file.close()
driver.quit()
