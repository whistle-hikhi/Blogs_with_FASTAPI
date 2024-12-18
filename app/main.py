from fastapi import FastAPI
from fastapi import Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class Blog(BaseModel):
    title: str
    content: str
    published: bool=True
while True:
    try:
        conn = psycopg2.connect(
            host=os.environ['host'],
            database=os.environ['database'],
            user=os.environ['user'],
            password=os.environ['password'],
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/login")
def read_book():
    return {"message": "Yahalo"}

@app.get("/blogs")
def get_blogs():
    cursor.execute("""SELECT * FROM public.blogs""")
    blogs = cursor.fetchall()
    return {"data": blogs}

@app.post("/make_blogs", status_code=status.HTTP_201_CREATED)
def make_blogs(blog: Blog):
    cursor.execute("""INSERT INTO public.blogs (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (blog.title, blog.content, blog.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": new_post}


@app.get("/blogs/{id}")
def get_blog(id: int):
    cursor.execute("""SELECT * FROM public.blogs WHERE id = %s""", (str(id),))
    blog = cursor.fetchone()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")

    return {"blog details": blog}

@app.delete("/blogs/{id}")
def delete_blog(id: int):

    cursor.execute("""DELETE FROM public.blogs WHERE id = %s RETURNING *""", (str(id),))
    deleted_blog = cursor.fetchone()
    conn.commit()

    if not deleted_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/blogs/{id}")
def update_blog(id: int, blog: Blog):
    cursor.execute("""UPDATE public.blogs SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (blog.title, blog.content, blog.published, str(id)))
    updated_blog = cursor.fetchone()
    conn.commit()
    if not updated_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")
    
    return {"data": updated_blog}