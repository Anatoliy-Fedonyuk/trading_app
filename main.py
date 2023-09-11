from pydantic import BaseModel, Field, PositiveInt
from uvicorn import run
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="Trading App")


# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"
@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=jsonable_encoder({"detail": exc.errors()}), )


fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"},
    {"id": 4, "role": "investor", "name": "Homer", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": ["expert"]}
    ]},
]


class DegreeType(Enum):
    newbie = "newbie"
    middle = "middle"
    expert = "expert"


class Degree(BaseModel):
    id: int = Field(ge=1)
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: PositiveInt = Field(ge=1)
    role: str
    name: str
    degree: None | list[Degree] = Field(None, description="Page about degree client")


@app.get("/users/{user_id}", response_model=list[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def get_trades(trades: list[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}



# if __name__ == "__main__":
#     run('main:app', reload=True)
