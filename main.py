from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/", summary='main route', tags=["Main"])
def start():
    return'Hi there'


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)