from pydantic import BaseModel

class AccelerometerData(BaseModel):
    accx: list
    accy: list
    accz: list
