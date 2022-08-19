#############################
## Importing the Libraries ##
#############################
import os
import time
from os import sep
from unicodedata import category
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException        

#######################################
## Scraping using Selenium Webdriver ##
#######################################

driver = webdriver.Firefox(executable_path=r'C:\Users\Neeraj Kankani\Downloads\geckodriver.exe')
coolcats_url = 'https://www.nft-stats.com/rarity/cool-cats-nft'
driver.get(coolcats_url)

##########################################
## Creating Data Frame for our CoolCats ##
###########################################

data = pd.DataFrame(columns=['cat_number', 'rank', 'face', 'face-score', 'shirt', 'shirt-score', 'body', 'tier', 'tier-score', 'hats', 'hats-score', 'Total'])
data

######################################################################
## Looping and scraping individual characteristics of all Cool Cats ##
######################################################################

for i in range(9932):

    input = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[1]/div/input')
    input.send_keys(i+1)
    
    just = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[1]/h1')
    just.click()
    time.sleep(0.1)
    row_dict = {}

    cat_number = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/span/h5').text
    row_dict['cat_number'] = cat_number

    face = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/div[1]/div/div[2]/table/tbody/tr[1]').text
    row_dict['face'] = face[5:]

    shirt = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/div[1]/div/div[2]/table/tbody/tr[2]').text
    row_dict['shirt'] = shirt[6:]

    body = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/div[1]/div/div[2]/table/tbody/tr[3]').text
    row_dict['body'] = body[5:]

    tier = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/div[1]/div/div[2]/table/tbody/tr[4]').text
    row_dict['tier'] = tier[5:]

    hats = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/div[1]/div/div[2]/table/tbody/tr[5]').text
    row_dict['hats'] = hats[5:]

    total = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/div[1]/div/div[2]/table/tbody/tr[6]').text
    row_dict['total'] = total[6:]

    close = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/div[2]/button').click()
    time.sleep(0.05)
    data = data.append(row_dict, ignore_index=True)


################################################################
## Looping and scraping ranking information for all Cool Cats ##
################################################################

nft_url = 'https://nftexp.io/explore/assets/cool-cats-nft'
driver.get(nft_url)

for _ in range(1000):

    for k in range(10):
        title_xpath = '/html/body/div/div/docsum-view/div/div/div[2]/ul/li[' + str(k+1) + ']/publication-view/div/div[2]/a'
        title = driver.find_element_by_xpath(title_xpath)
        row_dict = {}
        row_id = {}
        title.click()
        title_name = driver.find_element_by_css_selector('.publication-title').text
        id = driver.find_element_by_css_selector('.meta-item').text
        row_id['id'] = id
        print('id ', id)
        row_id['title'] = title_name
        print('title of article', title_name)
        rank = driver.find_element_by_xpath('//*[@id="rarityDiv"]/div/div/main/div[2]/div/div/span/h5/small').text
        row_dict['rank'] = rank
        # more = driver.find_element_by_css_selector('.visibility-toggle').click()
        # try:
        #     more = driver.find_element_by_css_selector('.visibility-toggle').click()
        # except NoSuchElementException:
        #     print('No more button')
        categories = driver.find_elements_by_css_selector('.table-section-name')
        print('categories ', categories)
        categories_dict = {}
        for i in range(len(categories)):
            category = categories[i]
            category_name = category.text
            category_list = []
            rows = driver.find_elements_by_xpath('/html/body/div/div/expanded-view/div/div/div[1]/summary/div/div[3]/div/table/tbody/tr')
            for j in range(len(rows)):
                keyword = rows[j].text
                category_list.append(keyword)
            categories_dict[category_name] = category_list
        row_dict = {**row_id, **categories_dict}
        data = data.append(row_dict, ignore_index=True)
        driver.back()
        time.sleep(0.25)
    next = driver.find_element_by_xpath('/html/body/div/div/docsum-view/div/div/div[2]/pagination[2]/span/span[2]')
    next.click()

#####################################
## Exporting Cool Cats data to CSV ##
#####################################

data.to_csv('data/scraped.csv')