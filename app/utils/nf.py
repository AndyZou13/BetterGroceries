from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine

import pandas as pd
import time

category = []

links = [["https://www.nofrills.ca/en/food/fruits-vegetables/fresh-fruits/c/28194", 4],
         ["https://www.nofrills.ca/en/food/fruits-vegetables/fresh-vegetables/c/28195", 7],
         ["https://www.nofrills.ca/en/food/fruits-vegetables/packaged-salad-dressing/c/28196", 2],
         ["https://www.nofrills.ca/en/food/fruits-vegetables/herbs/c/28197", 1], 
         ["https://www.nofrills.ca/en/food/fruits-vegetables/fresh-cut-fruits-vegetables/c/28198", 1], 
         ["https://www.nofrills.ca/en/food/fruits-vegetables/fresh-juice-smoothies/c/28200", 1]]

def freshScrape():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    for l in links:
        for i in range(l[1]):
            print(i)
            driver.get(f"{l[0]}?page={i+1}")
            time.sleep(5)
            freshElements = driver.find_elements(By.CSS_SELECTOR, "div[class='chakra-linkbox css-yxqevf']")
            for veg in freshElements:
                topContainer = veg.find_element(By.CSS_SELECTOR, "div[data-testid='price-product-tile']")
                productName = veg.find_element(By.CSS_SELECTOR, "h3[data-testid='product-title']").text
                productPriceQuant = veg.find_element(By.CSS_SELECTOR, "p[data-testid='product-package-size']")
                salePrice = topContainer.find_elements(By.CSS_SELECTOR, "span[data-testid='sale-price']")
                link = veg.find_element(By.CSS_SELECTOR, "a.chakra-linkbox__overlay").get_attribute("href")
                picture = veg.find_element(By.CSS_SELECTOR, 'img.chakra-image').get_attribute('src')
                isKG = False
                if salePrice:
                    if 'about' in salePrice[0].text:
                        salePrice = productPriceQuant.text[productPriceQuant.text.index('$'):productPriceQuant.text.index('/')]
                        isKG = True
                    else:
                        salePrice = salePrice[0].text[salePrice[0].text.index('$'):]
                    category.append({
                        "Source": "NF",
                        "Product Name": productName,
                        "Price": float(salePrice[1:]),
                        "isKG" : isKG,
                        "Link": link,
                        "Picture": picture,
                        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                else:
                    productPrice = topContainer.find_element(By.CSS_SELECTOR, "span[data-testid='regular-price']").text
                    if 'about' in productPrice:
                        productPrice = productPriceQuant.text[productPriceQuant.text.index('$'):productPriceQuant.text.index('/')]
                        isKG = True
                    category.append({
                        "Source": "NF",
                        "Product Name": productName,
                        "Price": float(productPrice[1:]),
                        "isKG" : isKG,
                        "Link": link,
                        "Picture": picture,
                        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

freshScrape()
          
df = pd.DataFrame(category)
df.to_csv("nf.csv", index=False)

engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/rpidb")

df.to_sql("your_table", engine, if_exists="append", index=False)