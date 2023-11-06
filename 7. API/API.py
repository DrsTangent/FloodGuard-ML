from typing import Union
import pickle
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

floodPredictor = pickle.load(open('model.pkl', 'rb'))


class Item(BaseModel):
    total_precipitation: float
    mean_2m_air_temperature: float
    year: int
    premWater: float
    month: int
    Lng: float
    area: float
    Lat: float
    Above_2500_percentage:float
    Below_118_percentage: float

@app.get('/prediction/')
def test(item: Item):
    data = [[item.month,
            item.year,
            item.Lat,
            item.Lng,
            item.mean_2m_air_temperature,
            item.total_precipitation,
            item.Above_2500_percentage,
            item.Below_118_percentage,
            item.premWater,
            item.area]]
    print(data)
    predict = floodPredictor.predict(data)
    return {"message": "oh war oye", "item": predict[0]}

@app.get('/test')
def here():
    return {"test": "working"}
