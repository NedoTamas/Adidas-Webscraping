import os
from datetime import date
import pandas as pd
import time

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
SKU = os.path.join(memory_path, str(today) + "_SKU.txt")
SKU_collected=os.path.join(memory_path, str(today) + "_SKU_collected.txt")

bronze_final = os.path.join(silver_path, '2025-01-04' + "_silver.csv")

# ---memory---
block_occured = False


def get_last_successful_item():
    try:
        with open(memory, "r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                item, status = line.strip().split(",")
                if status == "success":
                    return item
    except FileNotFoundError:
        return None
    return None


def update_memory(category_name, status):
    with open(memory, "a") as file:
        file.write(f"{category_name},{status}\n")


def memory_decision(block_occured, category_name):
    status = "403_error" if block_occured else "success"
    update_memory(category_name, status)

    if block_occured:
        print(f"403 error encountered for {category_name}. Stopping execution.")

def csv_to_list(file, i, filter=None, column=None):
    if os.path.isfile(file):
        df = pd.read_csv(file, header=None)
        if filter is None and column is None:
            result_list = df[i].tolist()
        elif filter is not None and column is not None:
            result_list = df[df[column] == filter][i].tolist()
        else:
            raise ValueError("Both filter and column must be provided or both must be None")
        return result_list
    else:
        print('Theres no such file')

def sleep_with_clock(duration):
    start_time = time.time()
    end_time = start_time + duration
    
    while time.time() < end_time:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        print(f"\rTime elapsed: {minutes:02d}:{seconds:02d}", end="", flush=True)
        time.sleep(0.1)
    
    print("\nSleep completed.")