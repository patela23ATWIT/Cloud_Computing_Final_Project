import mysql
import os
# Database connection
def connect_to_db():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("MYSQL_PASSWORD", ""),
            database="my_sporting_shop",
        )
        print("Successfully connected to MySQL database!")
        return mydb  # <-- Move this inside the try block!
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None  # Explicitly return None if connection fails

