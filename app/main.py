from fastapi import FastAPI
from app.routes import search, uploads
from app.database.mongo_database import client

app = FastAPI()

@app.get("/")
def home_test():
    data = client.TEST_DB.movies.find()
    return data.to_list()


# Include routes
app.include_router(uploads.router, tags=["Upload"])
app.include_router(search.router, tags=["Movies"])