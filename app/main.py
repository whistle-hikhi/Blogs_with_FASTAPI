from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import os
from dotenv import load_dotenv
import models
from database import engine
from routers import blog, user



models.Base.metadata.create_all(bind=engine)


load_dotenv()

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv('host'),
            database=os.getenv('database'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            port=os.getenv('port'),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(blog.router)

app.include_router(user.router)