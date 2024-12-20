from fastapi.testclient import TestClient
from app.main import app
from app.database.mongo_database import client as db_client
import os
import pytest
import random


client = TestClient(app)

# Setup and clear the test DB
test_db = db_client.TEST_DB
@pytest.fixture(autouse=True)
def setup_DB():
   test_db.movies.drop()
   yield

# Normal test to make sure the test DB is empty and endpoints can be hit
def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == []


# Test to make sure 400 is returned for an invalid file
def test_upload_invalid_file():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "wrong_file.txt")
    file = {"file": ("wrong_file.txt", open(file_path, "rb"))}
    response = client.post("/upload/upload-csv", files=file)

    assert response.status_code == 400


# Test to make sure 200 is returned for an valid file and saved to DB
def test_upload_valid_csv():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "data.csv")
    file = {"file": ("data.csv", open(file_path, "rb"))}
    response = client.post("/upload/upload-csv?testing=True", files=file)

    assert response.status_code == 200
    assert not test_db.movies.find().to_list() == []


# Test to make sure 200 is returned after searching
def test_search_after_upload():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "data.csv")
    file = {"file": ("data.csv", open(file_path, "rb"))}
    client.post("/upload/upload-csv?testing=True", files=file)

    response = client.get("/search/search-movies?testing=True")

    assert response.status_code == 200
    assert not response.json() == []


# Test to make sure the pagination length is correct
def test_search_pagination_length():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "data.csv")
    file = {"file": ("data.csv", open(file_path, "rb"))}
    client.post("/upload/upload-csv?testing=True", files=file)

    random_int = random.randint(1, 10)
    response = client.get(f"/search/search-movies?testing=True&limit={random_int}")

    assert response.status_code == 200
    assert len(response.json()) == random_int


# Test to make sure 400 is returned for an invalid query parameter
def test_search_incorrect_query_parameters():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "data.csv")
    file = {"file": ("data.csv", open(file_path, "rb"))}
    client.post("/upload/upload-csv?testing=True", files=file)

    invalid_sort_by_response = client.get(f"/search/search-movies?testing=True&sort_by=wrong")
    invalid_sort_order_response = client.get(f"/search/search-movies?testing=True&sort_order=50")

    assert invalid_sort_by_response.status_code == 400
    assert invalid_sort_order_response.status_code == 400


# Test to make sure the data is properly sorted
def test_search_sortby_and_sortorder():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "data.csv")
    file = {"file": ("data.csv", open(file_path, "rb"))}
    client.post("/upload/upload-csv?testing=True", files=file)

    response = client.get(f"/search/search-movies?testing=True&sort_by=vote_average&sort_order=-1")

    assert response.json()[0]['vote_average'] ==  10.0


# Test to make sure that the language filter is working
def test_search_language_filter():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "data.csv")
    file = {"file": ("data.csv", open(file_path, "rb"))}
    client.post("/upload/upload-csv?testing=True", files=file)

    response = client.get(f"/search/search-movies?testing=True&language=Français")

    assert response.json()[0]['original_language'] == "fr"


# Test to make sure year filter is working
def test_search_year_filter():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, "data.csv")
    file = {"file": ("data.csv", open(file_path, "rb"))}
    client.post("/upload/upload-csv?testing=True", files=file)

    response = client.get(f"/search/search-movies?testing=True&year=2017")

    assert response.json()[0]["release_date"].split("-")[0] == "2017"