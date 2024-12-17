from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_book():
    return {"message": "Hello World"}