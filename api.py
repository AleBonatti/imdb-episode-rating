import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from config import settings 

key = settings.imdb_key
app = FastAPI()

origins = [
    settings.api_url,
    settings.front_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Test"}

@app.get("/search")
async def search(text = None):
    if text is not None:
        response = requests.get(f"https://imdb-api.com/en/API/SearchSeries/{key}/{text}")
        dict = response.json()

        return dict
    else:
        return {}

@app.get("/details/{id}")
async def details(id):
    response = requests.get(f"https://imdb-api.com/en/API/Title/{key}/{id}")
    dict = response.json()
    return dict

@app.get("/episodes/{id}/{season}")
async def episodes(id, season):
    response = requests.get(f"https://imdb-api.com/en/API/SeasonEpisodes/{key}/{id}/{season}")
    dict = response.json()
    return dict

@app.get("/usage")
async def usage():
    response = requests.get(f"https://imdb-api.com/API/Usage/{key}")
    dict = response.json()
    #remaining = dict['maximum'] - dict['count']

    return dict