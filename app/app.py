from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import pandas as pd
from app.modules.pipeline import pipeline
from app.database import collection



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



@app.websocket("/socket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            df = pd.DataFrame(
                columns=['accx', 'accy', 'accz', 'long', 'lat', 'seconds'])

            # inserting the data into the dataframe. The data is expected to be a dictionary with the keys being the column names and lists as values
            for key in data.keys():
                df[key] = data[key]

            results = pipeline(df)
            print(results)

            # # uncomment this to save the poi to the database
            # results = pipeline(df)
            # for res in results:
            #     if res.res != 'normal':
            #         collection.insert_one(res.poi)
            

            await websocket.send_json({"results": results})

    except WebSocketDisconnect as e:
        print("WebSocket disconnected:", e)


## Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}
