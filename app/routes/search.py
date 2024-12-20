import app.schemas as schema
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.database.mongo_database import db, client

# Add search prefix to all endpoints in this route
router = APIRouter(
    prefix = "/search",
    tags = ['Search'],
)

# Endpoint to search through the uploaded movie data
# Pagination can be customised with limit parameter
# Can be filtered by language and/or year
# Can be sorted by release data/ratings ascending and descending
@router.get("/search-movies/", response_model=List[schema.MovieData])
async def get_movies(page: int = 1, limit: int = 10, year: int = None, language: str = None, sort_by: str = "release_date", sort_order: int = 1, testing=False):

    # If the query parameters are incorrect, return 400 bad req
    if not sort_by in ['release_date', 'vote_average']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" Invalid sort_by parameter. Must be 'release_date' or 'vote_average' ")
    if not sort_order in [1, -1]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid sort_order parameter. Must be 1 for ascending or -1 for descending.")

    database = db
    if testing:
        database = client.TEST_DB
    
    # Exception handling incase something goes wrong with the MongoDB query
    try:
        query = {}
        if year:
            # Look for occurences of the given year in 'release_date' using regex
            query["release_date"] = {"$regex": f"^{year}"}
        if language:
            # Look for occurences of the given language in the 'languages' array
            query["languages"] = language

        # Final query to get the items
        items = list(
            database.movies
            .find(query)
            .sort([(sort_by, sort_order)])
            .skip((page-1) * limit)
            .limit(limit)
            )

        # Convert the _id field in MongoDB to string before sending out the data
        final_data = []
        for item in items:
            item["_id"] = str(item["_id"])
            final_data.append(item)
    
    # Any error, return 500 with message saying error in query
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in querying data.")

    # Finally return the data
    return final_data
