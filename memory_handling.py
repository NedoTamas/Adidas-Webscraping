import os
from datetime import date 

#---pathing---
root = os.getcwd()
bronze_path=os.path.join(root,"bronze")
silver_path=os.path.join(root,"silver")
gold_path=os.path.join(root,"gold")
memory_path=os.path.join(root,"memory_log")

#---time---
today=date.today()

#---naming the output---
product_data_path=os.path.join(bronze_path, str(today)+'_product_data.csv')
product_data_availability_path=os.path.join(bronze_path, str(today)+'_product_data_availability.csv')
memory=os.path.join(memory_path, str(today)+'_memory.txt')
SKU=os.path.join(memory_path, str(today)+'_SKU.txt')

#---memory---
block_occured=False

def get_last_successful_item():
    try:
        with open(memory, "r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                item, status = line.strip().split(',')
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