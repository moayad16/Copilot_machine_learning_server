from fastapi import FastAPI, Request 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import pandas as pd
import numpy as np
from app.modules.pipeline import pipeline
from app.database import collection

app = FastAPI()





app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log the incoming request details
    logging.debug(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    # Log the response status code
    logging.debug(f"Response status code: {response.status_code}")

    return response


@app.get('/', tags=['root'])
async def root() -> dict:
    logging.debug("Root endpoint called.")
    return {"message": "Hello from your first FastApi project"}


@app.post('/data', tags=['data'])
async def postData(data:dict) -> dict:
    logging.debug("data endpoint called.")

    # creating a dataframe that will hold about 1000 roows of data
    df = pd.DataFrame(columns=['accx', 'accy', 'accz', 'long', 'lat', 'seconds'])

    # inserting the data into the dataframe. The data is expected to be a dictionary with the keys being the column names and lists as values
    for key in data.keys():
        df[key] = data[key]

    print(pipeline(df))

    return {
        "message": "Data recieved"
    }


@app.post('/test', tags=['test'])
async def testDb(data:dict) -> dict:
    print(data)
    collection.insert_one(data)
    return {
        "message": "data recieved"
    }
