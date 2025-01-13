from curl_cffi import requests
from bs4 import BeautifulSoup
import time
from random import randint
import pandas as pd
import os
import json
from datetime import date
from memory_handling import *
from credentials import headers, cookies 
from variables import countries
import multiprocessing

def raw_codes(category_name, country, paths):
    if os.path.isfile(paths['SKU_raw']):
        SKU_memory = csv_to_list(paths['SKU_raw'], 0, None, None)
        if SKU_memory[-1] == category_name:
            return SKU_memory
    
    base_url = f"{country}/{category_name}"
    all_item_code = []
    item_per_page = 48
    a = -item_per_page
    
    while True:
        try:
            a += item_per_page
            url = f"{base_url}?start={a}"
            response = requests.get(url, cookies=cookies, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            items = soup.find_all(
                "article",
                {"class": "product-card_product-card__a9BIh product-grid_product-card__8ufJk"}
            )

            if not items:
                print(f"{(a/item_per_page+1)} Pages were scraped")
                print(response)
                break

            for item in items:
                all_item_code.append(item.find("a").attrs["href"])
                print(item.find("a").attrs["href"])

        except Exception as e:
            print(f"An error has occurred: {e}")
            break
          
    all_item_code.append(category_name)
    df = pd.DataFrame(all_item_code)
    df.to_csv(paths['SKU_raw'], index=False, mode="w", header=None)
    return all_item_code

def codes(all_item_code, paths):
    if os.path.isfile(paths['SKU_list']):
        SKU_memory = csv_to_list(paths['SKU_list'], 0, None, None)
        if SKU_memory[-1] == 2:
            return SKU_memory[:-1]

    item_codes = [str(item)[-11:-5] for item in all_item_code[:-1]]
    item_codes.append(2)
    df = pd.DataFrame(item_codes)
    df.to_csv(paths['SKU_list'], index=False, mode="w", header=None)
    print("SKU list has been generated")
    
    return item_codes[:-1]

def details(item_codes, category_name, country, country_code, paths):
    if os.path.isfile(paths['SKU_list']):
        item_codes = csv_to_list(paths['SKU_list'], 0, None, None)[:-1]
    block_occurred = False
    i = 0
    
    if os.path.isfile(paths['product_data_path']):
        stored_data = csv_to_list(paths['product_data_path'], 1, category_name, column=3)
        stored_data = len(stored_data) if stored_data else 0
    else:
        stored_data = 0
    product_list = []

    for item in item_codes[stored_data:]:
        url = f"{country}/api/product-list/{item}"
        response = requests.get(url, cookies=cookies, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                product_data = data[0]
                product_info = {
                    "name": product_data.get("name"),
                    "id": product_data.get("id"),
                    "price": product_data.get("pricing_information", {}).get("currentPrice"),
                    "category": category_name,
                    "image_url": product_data.get("view_list", [{}])[0].get("image_url"),
                    "color": product_data.get("attribute_list", {}).get("color"),
                    "weight": product_data.get("attribute_list", {}).get("weight"),
                    "gender": product_data.get("attribute_list", {}).get("gender"),
                    "best_for_wear": next(iter(product_data.get("attribute_list", {}).get("best_for_ids", [])), None),
                    "date": str(date.today()),
                    "country_code": country_code
                }
                i += 1
                print(f"{i}th item in this cycle\n{product_info}")

                if i % 500 == 0:
                    time.sleep(randint(100, 150))

                product_list.append(product_info)
            else:
                print(f"No data found for item {item}")
        else:
            print(f"Failed to retrieve data for item {item}: {response.status_code}")
            if response.status_code == 403:
                block_occurred = True
                export(product_list, country_code, paths)
                break
    return product_list, block_occurred

def export(product_list, country_code, paths):
    df = pd.DataFrame(product_list)
    file_exists = os.path.isfile(paths['product_data_path'])
    df.to_csv(paths['product_data_path'], mode="a", header=not file_exists, index=False)
    print(f"{country_code}_product_data.csv generated in {paths['product_data_path']}")

def availability(country, country_code, paths):
    i = 0
    file_exists = os.path.isfile(paths['product_data_availability_path'])
    if file_exists:
        df = pd.read_csv(paths['product_data_availability_path'])
    else:
        df = pd.read_csv(paths['product_data_path'])
        print(f"There is no availability record stored for {country_code}. --- for now ;)")

    if "availability" not in df.columns:
        df["availability"] = None

    non_null_count = df["availability"].count()
    print(f"Number of non-null cells in 'availability' column: {non_null_count}")
    try:
        for index, row in df.iloc[non_null_count:].iterrows():
            i += 1
            id = row["id"]
            url = f"{country}/api/products/{id}/availability"

            response = requests.get(url, cookies=cookies, headers=headers, impersonate="chrome120")

            if i % 1 == 0:
                    time.sleep(randint(12, 13))

            if response.status_code == 200:
                print(f"{i}th item in this cycle\n")
                try:
                    data = json.loads(response.text)
                    variation_list = data.get("variation_list", [])

                    if variation_list:
                        availability_data = [
                            {"size": variation["size"], "availability": variation["availability"]}
                            for variation in variation_list
                        ]
                        df.at[index, "availability"] = json.dumps(availability_data)
                        print(f"Data found for {id}")
                    else:
                        print(f"No variation list found for product {id}")
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON for product {id}")
                except KeyError as e:
                    print(f"Unexpected response structure for product {id}: {e}")
            else:
                print(f"Failed to retrieve data for item {id}. response code: {response.status_code}")
                print("The script is quitting.")
                break
        print(f"Total data collected: {i-1}")
        df.to_csv(paths['product_data_availability_path'], index=False)
        print(f"Updated the availability for {country_code}.")
    except:
        print('Something happened, saving out the gathered data.')
        df.to_csv(paths['product_data_availability_path'], index=False)
        print(f"Updated the availability for {country_code}.")

def scrape_country(country_code, country_data):
    print(f"Processing country: {country_code}")
    
    paths = update_file_paths(country_code)

    i = 0
    last_successful_item = get_last_successful_item(country_code)
    country_categories = country_data['categories']
    start_index = (
        country_categories.index(last_successful_item) + 1
        if last_successful_item in country_categories
        else 0
    )
    for category_name in country_categories[start_index:]:
        i += 1
        all_item_code = raw_codes(category_name, country_data['url'], paths)
        item_codes = codes(all_item_code, paths)
        product_list, block_occurred = details(item_codes, category_name, country_data['url'], country_code, paths)
        memory_decision(block_occurred, category_name, country_code)
        if block_occurred:
            break
        export(product_list, country_code, paths)

    if i == 0:
        print(f"Today's category data gathering for {country_code} was already successful.")
    else:
        print(f"{i} categories data were collected in this cycle for {country_code}")

    availability(country_data['url'], country_code, paths)

def main():
    processes = []
    
    for country_code, country_data in countries.items():
        process = multiprocessing.Process(target=scrape_country, args=(country_code, country_data))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("Scraping completed for all countries.")

if __name__ == "__main__":
    main()
