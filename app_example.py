# 當爬取的網頁為 JavaScript 網頁前端（非伺服器端）生成，需引入 selenium 套件來模擬瀏覽器載入網頁並跑完 JavaScript 程式才能取得資料
# 引入套件
import time

import csv

import time

from selenium import webdriver
# 使用 WebDriverManager 下載和管理 ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup


# 使用 WebDriverManager 下載和管理 ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# 發出網路請求
driver.get('https://24h.pchome.com.tw/search/?q=手錶')


time.sleep(5)
"""
search_input = driver.find_elements_by_css_selector('#keyword')[0]
search_btn = driver.find_elements_by_css_selector('#btn_search')[0]
search_input.send_keys('手錶')
search_btn.click()
"""
time.sleep(10)
# 取出網頁整頁內容
page_content = driver.page_source

# 將 HTML 內容轉換成 BeautifulSoup 物件，html.parser 為使用的解析器
soup = BeautifulSoup(page_content, 'html.parser')

# 透過 select 使用 CSS 選擇器 選取我們要選的 html 內容
elements = soup.select('#ItemContainer .col3f')

row_list = []
for element in elements:
    product_name = element.select('.prod_name a')[0].text
    price = element.select('.price_box .price span')[0].text
    # 將資料整理成一個 dict
    data = {}
    data['product_name'] = product_name
    data['price'] = price
    row_list.append(data)
# CSV 檔案第一列標題會是 name, price，記得要和 dict 的 key 相同，不然會出現錯誤
headers = ['product_name', 'price']

# 使用檔案 with ... open 開啟 write (w) 寫入檔案模式，透過 csv 模組將資料寫入。使用 utf-8 避免中文亂碼，並設定 newline 去除空白行
with open('products.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, headers)
    # 寫入標題
    dict_writer.writeheader()
    # 寫入值
    dict_writer.writerows(row_list)
# 使用 with ... open 開啟讀取 read (r) 檔案模式，透過 csv 模組將已經存成檔案的資料讀入。使用 utf-8 避免中文亂碼，並設定 newline 去除空白行
with open('products.csv', 'r', newline='', encoding='utf-8') as input_file:
    rows = csv.reader(input_file)
    # 以迴圈輸出每一列，每一列是一個 list
    for row in rows:
        print(row)

driver.quit()