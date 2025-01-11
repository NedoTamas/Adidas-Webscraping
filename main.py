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

# Setting up variables

# ---pathing---
root = os.getcwd()
bronze_path = os.path.join(root, "bronze")
silver_path = os.path.join(root, "silver")
gold_path = os.path.join(root, "gold")
memory_path = os.path.join(root, "memory_log")

# ---time---
today = date.today()

# ---naming the output---
product_data_path = os.path.join(bronze_path, str(today) + "_product_data.csv")
product_data_availability_path = os.path.join(
    bronze_path, str(today) + "_product_data_availability.csv"
)
memory = os.path.join(memory_path, str(today) + "_memory.txt")
SKU = os.path.join(memory_path, str(today) + "_SKU.csv")
SKU_raw = os.path.join(memory_path, str(today) + "_SKU_raw.csv")

# ---memory---
block_occured = False


print(product_data_path)
print(product_data_availability_path)


# look for the "personalizationengine" POST request
# a cookie can survive circa 60 mins
# an ip can survive around 1000 requests for availability, after that you may have to get new cookies, or ip (connecting to a vpn)


#                                               ---Cookies / Headers from your browser---



category = [
    "sneakers",
    "fussball-schuhe",
    "outdoor-schuhe",
    "running-schuhe",
    "walking-schuhe",
    "fitness_training-schuhe",
    "tennis-schuhe",
]


# Old searching terms
# category=['manner-sneakers','frauen-sneakers','jungen-sneakers','manner-fitness_training-schuhe','manner-fussball-schuhe','manner-running-schuhe']
# Example url: https://www.adidas.de/manner-sneakers


def raw_codes(category_name):
    if os.path.isfile(SKU_raw):
        SKU_memory = csv_to_list(SKU_raw, 0, None, None)
        if SKU_memory[-1] == category_name:
            return SKU_memory
    
    base_url = f"https://www.adidas.de/{category_name}"
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


def details(item_codes, category_name):
    
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
        url = f"https://www.adidas.de/api/product-list/{item}"
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


def export(product_list, mode):
    df = pd.DataFrame(product_list)

    # if theres no existing file with this name, it saves the headers, otherwise just the records
    file_exists = os.path.isfile(product_data_path)

    df.to_csv(product_data_path, mode=mode, header=not file_exists, index=False)

    print(f"product_data.csv generated in {bronze_path}")


def availability():
    i = 0

    file_exists = os.path.isfile(product_data_availability_path)
    if file_exists:
        df = pd.read_csv(product_data_availability_path)
    else:
        df = pd.read_csv(product_data_path)
        print("There is no availability record stored. --- for now ;) ")

    if "availability" not in df.columns:
        df["availability"] = None

    non_null_count = df["availability"].count()
    print(f"Number of non-null cells in 'availability' column: {non_null_count}")
    try:
        for index, row in df.iloc[non_null_count:].iterrows():
            i = i + 1
            id = row["id"]
            url = f"https://www.adidas.de/api/products/{id}/availability"

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
        print("Updated the availability.")
    except:
        print('Something happened, saving out the gathered data.')
        df.to_csv(product_data_availability_path, index=False)
        print("Updated the availability.")

def main():
    i = 0
    last_successful_item = get_last_successful_item()
    start_index = (
        category.index(last_successful_item) + 1
        if last_successful_item in category
        else 0
    )
    for category_name in category[start_index:]:
        i = i + 1
        all_item_code = raw_codes(category_name)
        item_codes = codes(all_item_code)
        product_list, block_occured = details(item_codes, category_name)
        memory_decision(block_occured, category_name)
        if block_occured:
            break
        

    if i == 0:
        print("Today's category data gathering was already successful.")
    else:
        print(f"{i} categories data were collected in this cycle.")

    availability()


main()
