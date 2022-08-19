from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
driver = webdriver.Firefox(executable_path=r'C:\Users\Neeraj Kankani\Downloads\geckodriver.exe')
driver.get('https://cryptoslam.io/cool-cats#rarity')

html = driver.page_source
soup = BeautifulSoup(html)

with open ("data/pricing_source.html", 'w', encoding='utf-8') as f:
    f.write(html)


all_cards = soup.find_all("span", {"class":"rarities-cards__item-rank-rarity"})
cat_numbers = soup.find_all("p", {"class":"rarities-cards__item-name"})
cats = soup.find_all("div", {"class":"rarities-cards__item"})

len(all_cards)
len(cat_numbers)
len(cats)

price_data = pd.DataFrame(columns = ['number', 'price', 'currency'])

for cat in cats:
    row_dict = {}
    try:
        row_dict['number'] = cat.find("p", {"class":"rarities-cards__item-name"}).get_text()[10:]
        new_img = cat.find('img')
        parent_tag = new_img.parent
        price = float(parent_tag.find_next_sibling("span").get_text())
        row_dict['price'] = price
        row_dict['currency'] = cat.find("img")['data-original-title']
        print('number: ', row_dict['number'], '\nprice: ', row_dict['price'], 'currency: ', row_dict['currency'])
        price_data = price_data.append(row_dict, ignore_index=True)
    except:
        pass

len(price_data)
price_data.to_csv("data/price_data.csv", header=True)