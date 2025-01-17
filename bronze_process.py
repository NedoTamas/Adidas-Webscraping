
import pandas as pd
import json
import os
from datetime import date
from variables import *
from main import countries
from memory_handling import update_file_paths









def bronze_out(country_code):
    paths = update_file_paths(country_code)
    file_path = paths['product_data_availability_path']

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
                        #Not working cuz of US :) 'model_id' : str(id)+str(size_info['size']).strip().replace(" ", "").replace("/", ""),
                        'name': name,
                        'id': id,
                        'price': price,
                        'category': str(category).lstrip('en/').lstrip('us/'),
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



    processed_data.to_csv(paths['bronze_final'], index=False)


    print(f"Processed data has been saved to {silver_path}")







bronze_out()



    