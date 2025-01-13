import os
from datetime import date
import pandas as pd
import time
from variables import *



def update_file_paths(country_code):
    paths = {}
    paths['product_data_path'] = os.path.join(bronze_path, f"{country_code}_{str(today)}_product_data.csv")
    paths['product_data_availability_path'] = os.path.join(bronze_path, f"{country_code}_{str(today)}_product_data_availability.csv")
    paths['memory'] = os.path.join(memory_path, f"{country_code}_{str(today)}_memory.txt")
    paths['SKU_list'] = os.path.join(memory_path, f"{country_code}_{str(today)}_SKU.csv")
    paths['SKU_raw'] = os.path.join(memory_path, f"{country_code}_{str(today)}_SKU_raw.csv")
    paths['bronze_final'] = os.path.join(silver_path, f"{country_code}_{str(today)}_silver.csv")
    return paths

def get_last_successful_item(country_code):
    paths = update_file_paths(country_code)
    try:
        with open(paths['memory'], "r") as file:
            for line in reversed(file.readlines()):
                item, code, status = line.strip().split(",")
                if status == "success" and code == country_code:
                    return item
    except FileNotFoundError:
        return None
    return None

def update_memory(category_name, country_code, status):
    paths = update_file_paths(country_code)
    with open(paths['memory'], "a") as file:
        file.write(f"{category_name},{country_code},{status}\n")

def memory_decision(block_occurred, category_name, country_code):
    status = "403_error" if block_occurred else "success"
    update_memory(category_name, country_code, status)
    if block_occurred:
        print(f"403 error encountered for {category_name} in {country_code}. Stopping execution.")
    return block_occurred

def csv_to_list(file, i, filter=None, column=None):
    if os.path.isfile(file):
        df = pd.read_csv(file, header=None)
        if filter is None and column is None:
            return df[i].tolist()
        elif filter is not None and column is not None:
            if column not in df.columns:
                print(f"Warning: Column {column} not found. Available columns are: {df.columns}")
                return []
            return df[df[column] == filter][i].tolist()
        else:
            raise ValueError("Both filter and column must be provided or both must be None")
    else:
        print(f"File not found: {file}")
        return []

def sleep_with_clock(duration):
    start_time = time.time()
    end_time = start_time + duration
    
    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        print(f"\rTime elapsed: {minutes:02d}:{seconds:02d}", end="", flush=True)
        time.sleep(0.1)
    
    print("\nSleep completed.")