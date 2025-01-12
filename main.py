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
from variables import *
from memory_handling import update_file_paths



print(product_data_path)
print(product_data_availability_path)


# look for the "personalizationengine" POST request
# a cookie can survive circa 60 mins
# an ip can survive around 1000 requests for availability, after that you may have to get new cookies, or ip (connecting to a vpn)


#                                               ---Cookies / Headers from your browser---



#Dont forget to rename the existing csv files category!!!
countries = {
    'DE': {
        'url': 'https://www.adidas.de/',
        'categories': [
            "en/trainers",
            "en/fussball-schuhe",
            "en/outdoor-schuhe",
            "en/running-schuhe",
            "en/walking-schuhe",
            "en/fitness_training-schuhe",
            "en/tennis-schuhe",
        ]
    },
    'UK': {
        'url': 'https://www.adidas.co.uk/',
        'categories': [
            "trainers",
            "football-shoes",
            "outdoor-shoes",
            "running-shoes",
            "walking-shoes",
            "gym_training-shoes",
            "tennis-shoes",
        ]
    }
}


# Old searching terms
# category=['manner-sneakers','frauen-sneakers','jungen-sneakers','manner-fitness_training-schuhe','manner-fussball-schuhe','manner-running-schuhe']
# Example url: https://www.adidas.de/manner-sneakers


def raw_codes(category_name, country):
    if os.path.isfile(SKU_raw):
        SKU_memory = csv_to_list(SKU_raw, 0, None, None)
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
    df=pd.DataFrame(all_item_code)
    df.to_csv(SKU_raw, index=False, mode="w", header=None)
    return all_item_code

def codes(all_item_code):
    if os.path.isfile(SKU):
        SKU_memory=csv_to_list(SKU, 0, None, None)
        if SKU_memory[-1]==2:
            item_codes=SKU_memory[:-1]
            return item_codes

    item_codes = []
    for item in all_item_code[:-1]:
            
            item_codes.append(str(item)[-11:-5])
    

        # Saving out the codes to have a backup.                     // !!! Use it later to improve on the performance
    item_codes.append(2)
    df = pd.DataFrame(item_codes)
    df.to_csv(SKU, index=False, mode="w", header=None)
    print("SKU list has been generated")
        
    item_codes=item_codes[:-1]
    return item_codes


def details(item_codes, category_name, country, country_code):
    
    if os.path.isfile(SKU):
        item_codes = csv_to_list(SKU, 0, None, None)
        item_codes=item_codes[:-1]
    block_occured = False
    i = 0
    
    if os.path.isfile(product_data_path):
        stored_data = csv_to_list(product_data_path, 1, category_name, column=3)
        if stored_data is not None:
            stored_data = len(stored_data)
    else:
        stored_data = 0
    product_list = []

    for item in item_codes[stored_data:]:
        url = f"{country}/api/product-list/{item}"
        response = requests.get(url, cookies=cookies, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                product_data = data[0]  # Access the first item in the list
                product_info = {
                    "name": product_data.get("name", None),
                    "id": product_data.get("id", None),
                    "price": product_data.get("pricing_information", {}).get(
                        "currentPrice", None
                    ),
                    "category": category_name,
                    "image_url": product_data.get("view_list", [{}])[0].get(
                        "image_url", None
                    ),
                    "color": product_data.get("attribute_list", {}).get("color", None),
                    "weight": product_data.get("attribute_list", {}).get(
                        "weight", None
                    ),
                    "gender": product_data.get("attribute_list", {}).get(
                        "gender", None
                    ),
                    "best_for_wear": next(
                        iter(
                            product_data.get("attribute_list", {}).get(
                                "best_for_ids", []
                            )
                        ),
                        None,
                    ),
                    "date": str(today),
                    "country_code" : country_code
                }
                i = i + 1
                print(f"{i}.th item in this cycle\n{product_info}")

                # Implemented sleep to prevent ip blocks. //             !!! May lower in the future to secure smooth running
                if i % 500 == 0:
                    time.sleep(randint(100, 150))

                product_list.append(product_info)
            else:
                print(f"No data found for item {item}")
        else:
            print(f"Failed to retrieve data for item {item}: {response.status_code}")
            if response.status_code == 403:
                block_occured = True
                export(product_list, mode='a')
                break
    export(product_list, mode='a')
    return product_list, block_occured


def export(product_list, country_code):
    df = pd.DataFrame(product_list)
    file_exists = os.path.isfile(product_data_path)
    df.to_csv(product_data_path, mode="a", header=not file_exists, index=False)
    print(f"{country_code}_product_data.csv generated in {bronze_path}")



def availability(country, country_code):
    i = 0
    file_exists = os.path.isfile(product_data_availability_path)
    if file_exists:
        df = pd.read_csv(product_data_availability_path)
    else:
        df = pd.read_csv(product_data_path)
        print(f"There is no availability record stored for {country_code}. --- for now ;)")

    if "availability" not in df.columns:
        df["availability"] = None

    non_null_count = df["availability"].count()
    print(f"Number of non-null cells in 'availability' column: {non_null_count}")
    try:
        for index, row in df.iloc[non_null_count:].iterrows():
            i = i + 1
            id = row["id"]
            url = f"{country}/api/products/{id}/availability"

            response = requests.get(
                url, cookies=cookies, headers=headers, impersonate="chrome120"
            )

            # After 1000 requests we cause the server to block us. To prevent it implement waiting times.
            # Currently I have to reset my ip manually (connecting to a vpn, and disconnecting)
            # Previous tries: 2min/500r, 2min/350, 10m/700r, 20m/700r, 
            # 40m/700r-works->2838 requests, 
            if i % 700 == 0:
               sleep_with_clock(randint(2401,2420))

                # Enable it when I find a solution for proxy rotation
                # if response.status_code == 403:
                # rotate_VPN(settings)

            if response.status_code == 200:
                print(f"{i}.th item in this cycle\n")
                try:
                    data = json.loads(response.text)
                    variation_list = data.get("variation_list", [])

                    if variation_list:
                        availability_data = []
                        for variation in variation_list:
                            availability_data.append(
                                {
                                    "size": variation["size"],
                                    "availability": variation["availability"],
                                }
                            )
                        df.at[index, "availability"] = json.dumps(
                            availability_data
                        )  # Store as JSON string
                        print(f"Data found for {id}")
                    else:
                        print(f"No variation list found for product {id}")
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON for product {id}")
                except KeyError as e:
                    print(f"Unexpected response structure for product {id}: {e}")
            else:
                print(
                    f"Failed to retrieve data for item {id}. response code: {response.status_code}"
                )
                print("The script is quiting.")
                break
        print(f"Total data collected: {i-1}")
        df.to_csv(product_data_availability_path, index=False)
        print(f"Updated the availability for {country_code}.")
    except:
        print('Something happened, saving out the gathered data.')
        df.to_csv(product_data_availability_path, index=False)
        print(f"Updated the availability for {country_code}.")


def main():
    for country_code, country_data in countries.items():
        print(f"Processing country: {country_code}")
        
        # Update the file path for each country
        update_file_paths(country_code)

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
            all_item_code = raw_codes(category_name, country_data['url'])
            item_codes = codes(all_item_code)
            product_list, block_occurred = details(item_codes, category_name, country_data['url'], country_code)
            memory_decision(block_occurred, category_name, country_code)
            if block_occurred:
                break
            export(product_list, country_code)

        if i == 0:
            print(f"Today's category data gathering for {country_code} was already successful.")
        else:
            print(f"{i} categories data were collected in this cycle for {country_code}")

        availability(country_data['url'], country_code)


main()
