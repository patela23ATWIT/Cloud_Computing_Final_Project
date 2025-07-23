from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import os

app = FastAPI()

# Database connection
def connect_to_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD", ""),
            database="my_sporting_shop"
        )
        print("Successfully connected to MySQL database!")

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

    return mydb


# Get Query string parameter: /
@app.get("/")
async def root():
    return {"message": "Welcome to the Sporting Shop!"}
