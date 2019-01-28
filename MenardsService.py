from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
from MenardsEntity import *
from urllib import request
import os

# launch Menards url
url = "https://www.menards.com/main/search.html?sf_categoryHierarchy=&search=patio"

# Create a new Chrome session
driver = webdriver.Chrome()

# Wait for browser to load
driver.implicitly_wait(30)

# Go to url
driver.get(url)

# Pass page source from webdriver to BeautifulSoup constructor with html parser
soup_level1 = BeautifulSoup(driver.page_source, "html.parser")

# Finding all div tags with class of 'pod-inner' and storing them in soup_level2
soup_level2 = soup_level1.find_all('div', class_='ps-item')

# DataFrame reference variable
pageDataFrame = pd.DataFrame()

# Creating empty list
dataList = []

# Finding last breadcrumb link on page to make category name
lastBreadCrumb = soup_level1.find_all('div', class_='fontSegoeUI')[-1].text
category = str(lastBreadCrumb).replace(" ", "-").strip()


# Storing the path of the current directory for working file into var path
path = os.path.dirname(os.path.abspath(__file__))

# Changing to the directory for the working file
os.chdir(path)

# Creating a folder named 'Menards modelsku'
os.mkdir('Menardsimages')

# Changing to the directory for the working file
os.chdir(path)

# Find next button href for clicking to next page
# nextButton = driver.find_element_by_xpath('//*[@title="Next"]')

# Click the next button
# nextButton.click()

# Beautiful Soup finds all pod-inner class tags on the Home Depot page and the loop begins
for podInner in soup_level2:

    # Find div tag where class is 'ps-item-sku' for sku#/item num
    itemskuInfo = podInner.find('div', class_='ps-item-sku')

    #print(itemskuInfo)

    # Find div tag where class is 'ps-item-sku' for sku#/item num
    titleInfo = podInner.find('div', class_='ps-item-title')

    #print(titleInfo)

    # Pass item specific attributes to MenardsEntity constructor
    entity = MenardsEntity(itemskuInfo, titleInfo)

    # Convert entity fields to a dictionary for DataFrame conversion
    entityDict = vars(entity)

    # Extract dict from entityDict while removing dict_items enclosing
    newDict = dict(entityDict.items())

    # Enclose dict in brackets to pass into DataFrame constructor
    df = pd.DataFrame([newDict])

    # Append DataFrame to list of DataFrames
    dataList.append(df)

# Appending additional DataFrames together from dataList
pageDataFrame = pd.concat([pd.DataFrame(dataList[i]) for i in range(len(dataList))], ignore_index=True)

# Changing directory to the root project folder
os.chdir(path)

# Creating a Json folder for the json file of item data for page
os.mkdir('MenardsJson')

# Changing working directory to 'Json' folder
os.chdir('MenardsJson')

# Converting DataFrames to json and writing to file
pageDataFrame.to_json("menards_data.json", orient='records')

# Stop driver session
driver.quit()



