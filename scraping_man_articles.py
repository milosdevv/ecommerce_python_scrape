import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

baseurl = 'https://planetasport.rs/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

def collect_product_links(page):
    print(f'fetching page {page}')
    url = f'https://planetasport.rs/muskarci.html?p={page}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    productLinks = [
        item.find('a', href=True)['href'] 
        for item in soup.find_all('li', class_='product-item') 
        if item.find('a', href=True)
    ]
    return productLinks

def scrape_product_details(link):

    print(f"Scraping product: {link}")
    r = requests.get(link,headers=headers)
    soup = BeautifulSoup(r.content,'lxml')

    name_element = soup.find('h1',class_='page-title')
    name = None
    if name_element:
        name_span = name_element.find('span',class_='base')
        name = name_span.get_text(strip=True) if name_span else None
        
    price_elemets = soup.find_all('span',class_='price')
    price = price_elemets[0].get_text(strip=True) if price_elemets else None

    discount_elements_arr = []
    discount_elements = soup.find_all('div',class_='action-box-1')
    discount_elements_arr.append(discount_elements)

    if discount_elements_arr:
        discounts = [element.get_text(strip=True) for element in discount_elements[:2]]
    else:
        discounts = []
    
    image_wrap = soup.find('div',class_='easyzoom')
    image_urls = []
    if image_wrap:
        image_wrap_elements = image_wrap.find_all('img')
        image_urls = [img['src'] for img in image_wrap_elements if 'src' in img.attrs]

    return {'name': name, 'price': price, 'link': link, 'discounts':discounts,'product-image': image_urls}

def save_to_csv(data,filename='man_poducts.csv'):
     df = pd.DataFrame(data)
     df.to_csv(filename,index=False)
     print(f'Data saved to {filename}')


def main():
    print("STARTING SCRAPER")
    all_product_links = []

    for page in range(1):
        all_product_links.extend(collect_product_links(page))

    with ThreadPoolExecutor(max_workers=5) as executor:
        product_data = list(executor.map(scrape_product_details, all_product_links))

    save_to_csv(product_data)