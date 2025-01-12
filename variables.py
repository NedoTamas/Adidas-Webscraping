import os
from datetime import date



# Setting up variables

# ---pathing---
root = os.getcwd()
bronze_path = os.path.join(root, "bronze")
silver_path = os.path.join(root, "silver")
gold_path = os.path.join(root, "gold")
memory_path = os.path.join(root, "memory_log")
# ---time---
today = date.today()

#----naming the output---
# -----bronze-----
product_data_path = os.path.join(bronze_path, str(today) + "_product_data.csv")
product_data_availability_path = os.path.join(
    bronze_path, str(today) + "_product_data_availability.csv"
)

#------silver-----
bronze_final = os.path.join(silver_path, str(today) + "_silver.csv")
combined_silver=os.path.join(silver_path, 'combined_silver.csv')

# ---memory---
memory = os.path.join(memory_path, str(today) + "_memory.txt")
SKU = os.path.join(memory_path, str(today) + "_SKU.csv")
SKU_raw = os.path.join(memory_path, str(today) + "_SKU_raw.csv")
block_occured = False
SKU_collected=os.path.join(memory_path, str(today) + "_SKU_collected.txt")


#                                       // !!! Readable, but with scaling, change the declarations to be importable from a .py file



