from pydantic import BaseModel
from typing import List

class MovieData(BaseModel):
    budget: float
    homepage: str
    original_language: str
    original_title: str
    overview: str
    release_date: str 
    revenue: float
    runtime: int
    status: str
    title: str 
    vote_average: float
    vote_count: float
    production_company_id: int
    genre_id: int
    languages: List[str]