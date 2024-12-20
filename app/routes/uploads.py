from fastapi import APIRouter, UploadFile, HTTPException, File
from app.utils.CSV_handling import read_and_upload_CSV_data

router = APIRouter(
    prefix = "/upload",
    tags = ['Uploads'],
)

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):

    if not file.filename.endswith('.csv'):
       raise HTTPException(status_code=400, detail="Not a valid CSV file.")

    try:
        await read_and_upload_CSV_data(file)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error parsing CSV file")

    return {"message": "CSV uploaded successfully"}