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
    print("\n--- Axel Gerstl 開始 ---")
    driver = setup_driver()
    data = []
    try:
        url = "https://www.fiat500126.com/en/search?sSearch=clutch"
        print(f"URLへ移動中: {url}")
        driver.get(url)
        time.sleep(10) # 待ち時間を延長
        
        print(f"ページタイトル: {driver.title}") # ちゃんと開けたか確認
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select('.product--box')
        if not items: items = soup.select('.item')
        
        print(f"発見アイテム数: {len(items)}")
        
        for item in items[:5]:
            try:
                name_tag = item.select_one('.product--title') or item.select_one('.product--info a')
                price_tag = item.select_one('.product--price') or item.select_one('.price--content')
                
                if name_tag and price_tag:
                    name = name_tag.get_text(strip=True)
                    price = price_tag.get_text(strip=True)
                    print(f" - {name[:20]}... {price}")
                    data.append({"Shop": "Axel Gerstl", "Name": name, "Price": price})
            except Exception as e:
                print(f" アイテム解析エラー: {e}")
            
    except Exception as e:
        print(f"Axel 全体エラー: {e}")
    finally:
        driver.quit()
    return data

def scrape_passione():
    print("\n--- Passione 500 開始 ---")
    driver = setup_driver()
    data = []
    try:
        url = "https://www.passione500.it/ricerca?controller=search&s=frizione"
        print(f"URLへ移動中: {url}")
        driver.get(url)
        time.sleep(10) # 待ち時間を延長
        
        print(f"ページタイトル: {driver.title}")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select('.product-miniature')
        
        print(f"発見アイテム数: {len(items)}")
        
        for item in items[:5]:
            try:
                name_tag = item.select_one('.product-title a')
                price_tag = item.select_one('.price')
                
                if name_tag and price_tag:
                    name = name_tag.get_text(strip=True)
                    price = price_tag.get_text(strip=True)
                    print(f" - {name[:20]}... {price}")
                    data.append({"Shop": "Passione 500", "Name": name, "Price": price})
            except Exception as e:
                print(f" アイテム解析エラー: {e}")

    except Exception as e:
        print(f"Passione 全体エラー: {e}")
    finally:
        driver.quit()
    return data

if __name__ == "__main__":
    results = []
    
    # 実行
    results.extend(scrape_axel())
    results.extend(scrape_passione())
    
    # 結果が空でもCSVを作る（エラー確認用）
    if not results:
        print("\nデータが0件でしたが、空のCSVを作成します。")
        results.append({"Shop": "Error", "Name": "No Data Found", "Price": "0"})

    df = pd.DataFrame(results)
    print("\n=== 最終結果 ===")
    print(df)
    
    df.to_csv("parts_data.csv", index=False, encoding='utf-8-sig')
    print("CSV保存完了: parts_data.csv")
