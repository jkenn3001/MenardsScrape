from selenium import webdriver
from bs4 import BeautifulSoup
import string
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

#lastBreadCrumb = soup_level1.find_all('div', class_='fontSegoeUI')[-1].text
#category = str(lastBreadCrumb).replace(" ", "-").strip()
category = str('patioFurniture')


# Storing the path of the current directory for working file into var path
path = os.path.dirname(os.path.abspath(__file__))

# Changing to the directory for the working file
os.chdir(path)

# Creating a folder named 'Menardsimages'
os.mkdir('Menardsimages')

# Changing to the directory for the working file
os.chdir(path)

# Find next button href for clicking to next page

nextButton = driver.find_element_by_xpath('//*[@title="Next Page"]')

# Click the next button
# nextButton.click()

# Beautiful Soup finds all pod-inner class tags on Menards page and the loop begins
for podInner in soup_level2:

    # Find img tag where src contains '.jpg' for image url

    imageInfo = podInner.find('img', src=re.compile("(.*).jpg"))['src']
    imageInfo = 'http:' + imageInfo

    print(imageInfo)

    # Find div tag where class is 'ps-item-sku' for sku#/item num
    itemskuInfo = podInner.find('div', class_='ps-item-sku')
    #itemskuInfo = string.split(itemskuInfo, " ")[-1]
    #itemskuInfo = str(itemskuInfo.text).split() //took spaces out and put in array
    itemskuInfo = str(itemskuInfo.text).strip('\n').strip('\t').rstrip('\n').strip('Sku ').strip('#:').lstrip()
    #itemskuInfo = map(int, re.findall(r'\d+', itemskuInfo))
    #itemskuInfo = int(re.search(r'\d+', itemskuInfo).group())
    #[int(x.group()) for x in re.finditer(r'\d+', itemskuInfo)]
    #su = ''.join(x for x in itemskuInfo if x.isdigit())
   # itemskuInfo = " ".join(itemskuInfo.split())
   # itemskuInfo = "".join(line.strip() for line in itemskuInfo.split("\n"))
    #print int(filter(str.isdigit, itemskuInfo))
    print('sku#' + itemskuInfo)

    # Extracting sku number from itemsku num

    #skuNumber = str(itemskuInfo.text).strip().split(" ")[1].strip()

    skuNumber = str(itemskuInfo)

    # Concatenating category and skuNumber to create the folder name for searched item images
    folderName = category + "-" + skuNumber

    # Creating the filename for the jpg image files
    fileName = str(imageInfo.split('/')[-1])

    # Changing directory to the Images folder
    os.chdir('Menardsimages')

    # Making the folder based on folderName
    os.mkdir(folderName)

    # Changing current directory to Images folder
    os.chdir(folderName)

    # Sending request to download image and store with proper filename
    request.urlretrieve(imageInfo, fileName)


    # Resetting current directory to parent directory of Images folder
    os.chdir(path)

    # Find div tag where class is 'ps-item_title' for item
    titleInfo = podInner.find('div', class_='ps-item-title')
    #print object  title and accompanying info

    # Find div tag where class is 'price__numbers' for pricing information
    priceInfo = podInner.find('span', class_='priceInfo')
    print(priceInfo)

    # Pass item specific attributes to MenardsEntity constructor
    entity = MenardsEntity(itemskuInfo, titleInfo, priceInfo, imageInfo)

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



