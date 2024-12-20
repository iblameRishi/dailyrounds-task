from fastapi import FastAPI
from app.routes import search, uploads

app = FastAPI()

# Include routes
app.include_router(uploads.router, tags=["Upload"])
app.include_router(search.router, tags=["Movies"])