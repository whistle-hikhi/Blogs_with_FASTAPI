from fastapi import FastAPI
from fastapi import Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Blog(BaseModel):
    title: str
    content: str
    published: bool=True
    score: Optional[int]=None

my_blogs = [{
    "title": "My first blog",
    "content": "This is my first blog",
    "published": True,
    "score": 8,
    "id": 1
},
{
    "title": "How to make a blog",
    "content": "You need to know how to write a blog",
    "published": True,
    "score": 9,
    "id": 2}]

def find_blog(id):
    for blog in my_blogs:
        if blog["id"] == id:
            return blog
@app.get("/login")
def read_book():
    return {"message": "Yahalo"}

@app.get("/blogs")
def get_blogs():
    return {"data": my_blogs}

@app.post("/make_blogs")
def make_blogs(blog: Blog):
    blog_dict = blog.model_dump()
    blog_dict["id"] = randrange(0, 1000000)
    my_blogs.append(blog_dict)
    return {"message": blog_dict}


@app.get("/blogs/{id}")
def get_blog(id: int):
    blog = find_blog(id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Blog with id {id} does not exist"}
    return {"blog details": blog}

@app.delete("/blogs/{id}")
def delete_blog(id: int):
    blog = find_blog(id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")
    my_blogs.remove(blog)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/blogs/{id}")
def update_blog(id: int, blog: Blog):
    blog_index = find_blog(id)
    if not blog_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")
    blog_index.update(blog.model_dump())
    return {"data": blog_index}