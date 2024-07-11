import random
import time

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup


import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ExpectedConditions
import pandas as pd
import time
# from fake_useragent import UserAgent
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



import pandas as pd
import numpy as np
import re

service = Service(executable_path='./msedgedriver.exe')
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')

driver = webdriver.Edge(service=service, options=options)
url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi"
driver.get(url)
i = 1
while True:
    i = i + 1
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
    # ----------------Ghi ra file CSV ---------------
    result = df_elements  # Khởi tạo DataFrame kết quả với dữ liệu từ trang đầu tiên
    sleep(2)
    #click_btn = driver.find_element(By.XPATH, "./html/body/div[7]/div[2]/div[2]/div[6]/div/a[7]/i").click()
    try:
        reuw = "//a[@href= '/ban-can-ho-chung-cu-ha-noi/p{}']"
        nextButton = driver.find_element(By.XPATH,reuw.format(i) )
        WebDriverWait(driver, 5000).until(ExpectedConditions.element_to_be_clickable(nextButton))
        driver.execute_script("arguments[0].click();", nextButton)
    except NoSuchElementException:
        print("Breaking as Last page Reached")
        break
    print("______________________")
    sleep(10)
sleep(3)
# for i in range(2, 5):
#     print("Page : " + str(i))
#     url = "https://batdongsan.com.vn/ban-can-ho-chung-cu-ha-noi/p{}".format(i)
#
#     driver.execute_script("window.open('{}', '_blank')".format(url))
#     time.sleep(4)
#     driver.switch_to.window(driver.window_handles[1])
#     driver.switch_to.frame(0)
#     driver.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input').click()
#
#     elems = driver.find_elements(By.CSS_SELECTOR, ".js__product-link-for-product-id")
#     title = [elem.find_element(By.CSS_SELECTOR, '.pr-title.js__card-title').text for elem in elems]
#     links = [link.get_attribute("href") for link in elems]
#
#     prices = [price.find_element(By.CSS_SELECTOR, ".re__card-config-price.js__card-config-item").text for price in
#               elems]
#     squares = [square.find_element(By.CSS_SELECTOR, ".re__card-config-area.js__card-config-item").text for square in
#                elems]
#     location = [re.sub(r'\s+', ' ', loc.find_element(By.CSS_SELECTOR, '.re__card-location').text.strip('·')) for loc in
#                 elems]
#     price_per_m2 = []
#     for ppm in elems:
#         try:
#             price_per_m2.append(
#                 ppm.find_element(By.CSS_SELECTOR, ".re__card-config-price_per_m2.js__card-config-item").text)
#         except NoSuchElementException:
#             price_per_m2.append("N/A")  # Nếu không tìm thấy, thêm giá trị "N/A" vào danh sách
#     # -----------------Tạo DataFrame------------------
#     df_elements_i = pd.DataFrame(list(zip(title, prices, squares, price_per_m2, location, links)),
#                                columns=["Title", "Price", "Square", "Price_per_m2", "Location", "Link"])
#     result = pd.concat([result,df_elements_i])
#     # Chờ một khoảng thời gian ngẫu nhiên trước khi điều hướng tới trang tiếp theo
#     sleep(10)
#
# # Thiết lập lại chỉ mục cho DataFrame kết quả
# result.reset_index(drop=True, inplace=True)
# result.insert(0, "Index", range(1, len(result) + 1))
#
# # Ghi ra file CSV
result.to_csv("data.csv", index=False)
sleep(5)

driver.quit()

