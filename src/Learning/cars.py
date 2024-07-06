from fastapi import *
from pydantic import BaseModel, Field 
from typing import *
from auth_router import route



class Car:
    id: int
    name: str
    color: str
    avaliable: bool
    
    def __init__(self, id, name, color, avaliable): 
        self.id = id
        self.name = name
        self.color = color
        self.avaliable = avaliable

class CarBaseModle(BaseModel):
    id: int | None=None
    name: str = Field(min_length = 3)
    color: str = Field(min_length = 3)
    avaliable: bool 
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "A very nice Item",
                    "color": "bad",
                    "avaliable": False,
                }
            ]
        }
    }


app = FastAPI()
app.include_router(route)

cars = [
    Car(1, "Maruti 800", "Red", False),
    Car(2, "Ritz", "Silver", False),
    Car(3, "Nano", "Blue", False),
    Car(4, "Honda City", "Silver", True),
    Car(5, "Baleno", "Red", True)
]


@app.get("/cars")
def getCars():
    return cars

@app.post("/addcar", status_code=status.HTTP_201_CREATED)
def addCar(newCar: CarBaseModle):
    newCar.id = cars[-1].id+1
    car = Car(**newCar.model_dump())
    cars.append(car)
    return 

@app.delete("/deletecarbyidquery", status_code=status.HTTP_202_ACCEPTED)
def deleteCarByQuery(car_id:int = Query(gt=0, lt=10)):
    for i in range(0, len(cars)):
        if cars[i].id==car_id:
            cars.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID not found")

@app.delete("/deletecarbyidPath/{car_id}", status_code=status.HTTP_202_ACCEPTED)
def deleteCarByPath(car_id:int = Path(gt=0, lt=10)):
    for i in range(0, len(cars)):
        if cars[i].id==car_id:
            cars.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID not found")

def add_record():
    cars.append(None)

@app.get("/carsdepends")
def dependencyInjection(fgh: Annotated[None, Depends(add_record)]):
    return cars

    