
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from time import sleep
import os
import base64

# 初始化 Selenium webdriver
driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.pinterest.com/oxxostudio/outdoor/')
imgCount = driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="pin-count"]')
count = int(imgCount.text.split(' ')[0])

scroll = 0
# 建立資料夾以存儲圖片
os.makedirs('downloaded_images', exist_ok=True)

# 定義下載圖片函數
def download_images():
    global scroll
    scroll += 450
    driver.execute_script(f'window.scrollTo(0, {scroll})')
    sleep(0.5)
    # 使用 BeautifulSoup 提取所有圖片元素
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    imgs = soup.select('div[data-test-id="pin"] img')
    for img in imgs:
        try:
            url = img['src']
            # 取得圖片名稱
            name = url.split('/')[-1].split('?')[0]
            # 下載圖片   # 讀取圖片二進位數據
            image_data = driver.execute_script(f"return fetch('{url}').then(res => res.blob());")
            with open(f'downloaded_images/{name}', 'wb') as f:
                f.write(base64.b64decode(image_data['data']))
            print(f'圖片 {name} 下載完成')
        except KeyError:
            continue
# 重複捲動直到獲得足夠數量的圖片
while True:
    download_images()
    if len([file for file in os.listdir('downloaded_images') if file.endswith('.jpg')]) >= count:
        break

# 取得所有下載的圖片檔案名稱
image_filenames = [file for file in os.listdir('downloaded_images') if file.endswith('.jpg')]


# 將圖片檔案名稱寫入 CSV 檔案
with open('./image_filenames.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['image_filename'])
    writer.writerows([[filename] for filename in image_filenames])

print("圖片檔案名稱已儲存到: image_filenames.csv")

# 關閉瀏覽器
driver.quit()
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
from time import sleep
import os
import base64
import requests

# 初始化 Selenium webdriver
driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.pinterest.com/oxxostudio/outdoor/')
imgCount = driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="pin-count"]')
count = int(imgCount.text.split(' ')[0])

scroll = 0

# 建立資料夾以存儲圖片
os.makedirs('downloaded_images', exist_ok=True)

# 創建一個空的字典來存儲圖片文件名
image_data = {}

# 定義下載圖片函數
def download_images():
    global scroll
    scroll += 450
    driver.execute_script(f'window.scrollTo(0, {scroll})')
    sleep(0.5)
    # 使用 BeautifulSoup 提取所有圖片元素
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    imgs = soup.select('div[data-test-id="pin"] img')
    for img in imgs:
        try:
            url = img['src']
            # 取得圖片名稱
            name = url.split('/')[-1].split('?')[0]
            # 下載圖片   # 讀取圖片二進位數據
            response = requests.get(url)
            sleep(0.5)
            with open(f'downloaded_images/{name}', 'wb') as f:
                f.write(response.content)
            print(f'圖片 {name} 下載完成')
            # 將圖片文件名存入字典
            image_data[name] = url
        except KeyError:
            continue
# 重複捲動直到獲得足夠數量的圖片
while True:
    download_images()
    if len([file for file in os.listdir('downloaded_images') if file.endswith('.jpg')]) >= count:
        break

# 取得所有下載的圖片檔案名稱
image_filenames = [file for file in os.listdir('downloaded_images') if file.endswith('.jpg')]


# 將圖片檔案名稱寫入 CSV 檔案
with open('image_filenames.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['image_filename', 'image_url'])
    writer.writerows([[filename] for filename in image_filenames])

print("圖片檔案名稱已儲存到: image_filenames.csv")

# 關閉瀏覽器
driver.quit()

