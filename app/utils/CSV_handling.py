import csv
from app.database.mongo_database import client
import ast

# Util Function to parse and save the movie data thats in the CSV file
async def read_and_upload_CSV_data(file, testing):
   db = client['TEST_DB'] if testing else client['imdb_task']
   contents = await file.read()  
   decoded_contents = contents.decode()
   reader = csv.DictReader(decoded_contents.splitlines())

   # Some preprocessing, like making the numbers into int or float types instead of string and making sure the languages array is saved as an actual array
   data_to_insert = []
   for row in reader:
      if isinstance(row['languages'], str):
         try:
            # I have used the ast module to safely parse the string, and make sure no harmful content is being executed/processed
            row['languages'] = ast.literal_eval(row['languages'])
         except (ValueError, SyntaxError):
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
    
   # Save to DB
   db.movies.insert_many(data_to_insert)
   print("Data uploaded successfully")