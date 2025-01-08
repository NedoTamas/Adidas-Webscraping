
import pandas as pd
import json
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

#                                       // !!! Readable, but with scaling, change the declarations to be importable from a .py file
product_data_availability_path=os.path.join(bronze_path, str(today)+'_product_data_availability.csv')
bronze_final=os.path.join(bronze_path, str(today)+'_bronze_process.csv')


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
                    'gender' : gender
                    
                }
                records.append(record)
        except json.JSONDecodeError:
            print(f"Invalid JSON: {index}. line: {row['availability']}")


processed_data = pd.DataFrame(records)



processed_data.to_csv(bronze_final, index=False)


print(f"Processed data has been saved to {bronze_path}")