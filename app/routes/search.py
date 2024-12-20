import app.schemas as schema
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database.mongo_database import db

router = APIRouter(
    prefix = "/search",
    tags = ['Search'],
)

@router.get("/search-movies/", response_model=List[schema.MovieData])
async def get_movies(page: int = 1, limit: int = 10, year: int = None, language: str = None, sort_by: str = "release_date", sort_order: int = 1):

    if not sort_by in ['release_date', 'vote_average']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" Invalid sort_by parameter. Must be 'release_date' or 'vote_average' ")
    if not sort_order in [1, -1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sort_order parameter. Must be 1 for ascending or -1 for descending.")

    try:
        query = {}
        if year:
            query["release_date"] = {"$regex": f"^{year}"}
        if language:
            query["languages"] = language

        items = list(
            db.movies
            .find(query)
            .sort([(sort_by, sort_order)])
            .skip((page-1) * limit)
            .limit(limit)
            )

        final_data = []
        for item in items:
            item["_id"] = str(item["_id"])
            final_data.append(item)
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in querying data.")


    return final_data
