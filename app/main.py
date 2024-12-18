from fastapi import FastAPI
from fastapi import Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
import models
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from fastapi.params import Depends

models.Base.metadata.create_all(bind=engine)


load_dotenv()

app = FastAPI()

class Blog(BaseModel):
    title: str
    content: str
    published: bool=True
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv('host'),
            database=os.getenv('database'),
            user=os.getenv('user'),
            password=os.getenv('password'),
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
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return {"data": blogs}

@app.post("/make_blogs", status_code=status.HTTP_201_CREATED)
def make_blogs(blog : Blog, db: Session = Depends(get_db)):
    
    new_blog = models.Blog(**blog.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog}


@app.get("/blogs/{id}")
def get_blog(id: int, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")

    return {"blog details": blog}

@app.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db)):

    deleted_blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog = deleted_blog.first()
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")

    deleted_blog.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/blogs/{id}")
def update_blog(id: int, blog: Blog, db: Session = Depends(get_db)):
    updated_blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog = updated_blog.first()
    
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")
    
    updated_blog.update(blog.model_dump())
    db.commit()
    return {"data": updated_blog}