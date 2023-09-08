from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


@app.get("/")
def hello():
    return "Hello world !"


if __name__ == "__main__":
    run('main:app', host="127.0.0.1", port=8000, reload=True)
