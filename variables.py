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
SKU_list = os.path.join(memory_path, str(today) + "_SKU.csv")
SKU_raw = os.path.join(memory_path, str(today) + "_SKU_raw.csv")
block_occured = False
SKU_collected=os.path.join(memory_path, str(today) + "_SKU_collected.txt")


#Dont forget to rename the existing csv files category!!!


#If the category is non existent, the program goes into an infinite loop. Find an error handling for that.
countries = {
    'DE': {#Done
        'url': 'https://www.adidas.de/',
        'categories': [
            "en/trainers",
            "en/football-shoes",
            "en/outdoor-shoes",
            "en/running-shoes",
            "en/walking-shoes",
            "en/gym_training-shoes",
            "en/tennis-shoes",
        ]
    },
    'UK': {#Done
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
    },
    'BE':{#Done
        'url': 'https://www.adidas.be/',
        'categories': [
            "en/trainers",
            "en/football-shoes",
            "en/outdoor-shoes",
            "en/running-shoes",
            "en/walking-shoes",
            "en/gym_training-shoes",
            "en/tennis-shoes",
        ]
    },
    'US':{#Done
        'url': 'https://www.adidas.com/',
        'categories': [
            "us/athletic_sneakers",
            "us/soccer-shoes",
            "us/hiking-shoes",
            "us/running-shoes",
            "us/walking-shoes",
            "us/workout-shoes",
            "us/tennis-shoes",
        ]
    }
}



