from fastapi import APIRouter, UploadFile, HTTPException, File
from app.utils.CSV_handling import read_and_upload_CSV_data

# Add upload prefix to all endpoints in this route
router = APIRouter(
    prefix = "/upload",
    tags = ['Uploads'],
)

# Endpoint to upload CSV file data
@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), testing=False):

    # If its nto a csv file, return 400
    if not file.filename.endswith('.csv'):
       raise HTTPException(status_code=400, detail="Not a valid CSV file.")

    # Exception Handling incase something goes wrong with parsing CSV file
    try:
        # This func is in the utils folder, parses the file and saves data to DB
        await read_and_upload_CSV_data(file, testing)
    
    # If anything goes wrong return 500
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error parsing CSV file")

    # Return success message
    return {"message": "CSV uploaded successfully"}