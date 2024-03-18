from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
import numpy as np
import re

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi"
driver.get(url)
#------------------------ GET Title/Link-----------
elems = driver.find_elements(By.CSS_SELECTOR, ".js__product-link-for-product-id")
title = [elem.find_element(By.CSS_SELECTOR, '.pr-title.js__card-title').text for elem in elems]
links = [link.get_attribute("href") for link in elems]

prices = [price.find_element(By.CSS_SELECTOR, ".re__card-config-price.js__card-config-item").text for price in elems]
squares = [square.find_element(By.CSS_SELECTOR, ".re__card-config-area.js__card-config-item").text for square in elems]
location = [re.sub(r'\s+', ' ', loc.find_element(By.CSS_SELECTOR, '.re__card-location').text.strip('·')) for loc in elems]

price_per_m2 = []
for ppm in elems:
    try:
        price_per_m2.append(ppm.find_element(By.CSS_SELECTOR, ".re__card-config-price_per_m2.js__card-config-item").text)
    except NoSuchElementException:
        price_per_m2.append("N/A")  # Nếu không tìm thấy, thêm giá trị "N/A" vào danh sách
#-----------------Tạo DataFrame------------------
df_elements = pd.DataFrame(list(zip(title, prices, squares, price_per_m2, location, links)), columns = ["Title", "Price", "Square", "Price_per_m2", "Location", "Link"])
df_elements.insert(0, "Index", range(1, len(df_elements) + 1))
# ----------------Ghi ra file CSV ---------------
df_elements.to_csv("data.csv", index=False)

sleep(3)
driver.quit()

