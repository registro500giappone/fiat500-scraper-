import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_axel():
    print("--- Axel Gerstl 開始 ---")
    driver = setup_driver()
    data = []
    try:
        url = "https://www.fiat500126.com/en/search?sSearch=clutch"
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select('.product--box')
        if not items: items = soup.select('.item')
        print(f"Axel: {len(items)} 件発見")
        for item in items[:5]:
            try:
                name = item.select_one('.product--title').get_text(strip=True)
                price = item.select_one('.product--price').get_text(strip=True)
                data.append({"Shop": "Axel Gerstl", "Name": name, "Price": price})
            except: pass
    except Exception as e:
        print(f"Axel Error: {e}")
    finally:
        driver.quit()
    return data

def scrape_passione():
    print("--- Passione 500 開始 ---")
    driver = setup_driver()
    data = []
    try:
        url = "https://www.passione500.it/ricerca?controller=search&s=frizione"
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select('.product-miniature')
        print(f"Passione: {len(items)} 件発見")
        for item in items[:5]:
            try:
                name = item.select_one('.product-title a').get_text(strip=True)
                price = item.select_one('.price').get_text(strip=True)
                data.append({"Shop": "Passione 500", "Name": name, "Price": price})
            except: pass
    except Exception as e:
        print(f"Passione Error: {e}")
    finally:
        driver.quit()
    return data

if __name__ == "__main__":
    results = []
    results.extend(scrape_axel())
    results.extend(scrape_passione())
    
    if results:
        df = pd.DataFrame(results)
        print(df)
        df.to_csv("parts_data.csv", index=False, encoding='utf-8-sig')
        print("CSV保存完了")
    else:
        print("データなし")
