import csv
from app.database.mongo_database import db
import ast

async def read_and_upload_CSV_data(file):

   contents = await file.read()  
   decoded_contents = contents.decode()
   reader = csv.DictReader(decoded_contents.splitlines())

   data_to_insert = []
   for row in reader:
      # Check if 'languages' is a string representation of a list
      if isinstance(row['languages'], str):
         try:
               # Safely evaluate the string to a list
               row['languages'] = ast.literal_eval(row['languages'])
         except (ValueError, SyntaxError):
               # Handle cases where the conversion fails
               row['languages'] = []
         finally:
            row['budget'] = float(row['budget'])
            row['revenue'] = float(row['revenue'])
            row['runtime'] = int(row['runtime'])
            row['vote_average'] = float(row['vote_average'])
            row['vote_count'] = float(row['vote_count'])
            row['production_company_id'] = int(row['production_company_id'])
            row['genre_id'] = int(row['genre_id'])

            data_to_insert.append(row)
    
   db.movies.insert_many(data_to_insert)
   print("Data uploaded successfully")