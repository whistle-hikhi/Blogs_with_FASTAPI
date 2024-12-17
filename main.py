from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Blog(BaseModel):
    title: str
    content: str
    published: bool=True
    score: Optional[int]=None

@app.get("/login")
def read_book():
    return {"message": "Yahalo"}

@app.get("/blogs")
def get_blogs():
    return {"data": "This is a blog of u"}

@app.post("/make_blogs")
def make_blogs(blog: Blog):
    return {"message": blog.model_dump()}