
import pandas as pd
import json
import os
from datetime import date
from variables import *
from main import countries
from memory_handling import update_file_paths









def bronze_out(country_code):
    file_path = product_data_availability_path

    data = pd.read_csv(file_path)
    records = []
    for index, row in data.iterrows():
        
        name = row.get('name', None)
        id = row.get('id', None)
        price = row.get('price', None)
        category = row.get('category', None)
        image_url = row.get('image_url', None)
        color = row.get('color', None)
        weight = row.get('weight', None)
        best_for_wear = row.get('best_for_wear', None)
        gender = row.get('gender', None)
        datum = row.get('date', None)
        country_code = row.get('country_code', None)

    
        if pd.notna(row['availability']):
            try:
                availability_list = json.loads(row['availability'])
                for size_info in availability_list:
                    record = {
                        'model_id' : str(id)+str(size_info['size']).strip().replace(" ", "").replace("/", ""),
                        'name': name,
                        'id': id,
                        'price': price,
                        'category': category,
                        'color': color,
                        'weight': float(weight),
                        'best_for_wear': best_for_wear,
                        'size': size_info['size'],
                        'availability': size_info['availability'],
                        'image_url': image_url,
                        'gender' : gender,
                        'date': datum,
                        'country_code' : country_code
                        
                    }
                    records.append(record)
            except json.JSONDecodeError:
                print(f"Invalid JSON: {index}. line: {row['availability']}")


    processed_data = pd.DataFrame(records)



    processed_data.to_csv(bronze_final, index=False)


    print(f"Processed data has been saved to {silver_path}")



def append_files():
    file_list=[]
    exists = os.path.isfile(combined_silver)
    #During testing I had to append multiple files at once, but it won't be neccessary once everything runs smoothly.
    for country_code, country in countries.items():
        # Update the file path for each country
        update_file_paths(country_code)
        file_list.append(bronze_final)
            
                 

    df_list = [pd.read_csv(file) for file in file_list]

    combined_df = pd.concat(df_list, ignore_index=True)

    combined_df.to_csv(combined_silver, index=False, header=not exists, mode='a')

def main_bronze():
    update_file_paths(country_code)
    for country_code, country in countries.items():
        bronze_out(country_code)
    append_files()

    