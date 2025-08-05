import secrets
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from api.db import connect_to_db

app = FastAPI()

class CookieIssueRequest(BaseModel):
    email_address: str
    password: str

@app.post("/cookies/issue")
async def issue_cookie(data: CookieIssueRequest):
    expire_minutes: int = 60
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # Authenticate admin (plaintext password for now)
    check_query = "SELECT admin_id FROM administrators WHERE email_address = %s AND password = %s"
    cursor.execute(check_query, (data.email_address, data.password))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")
    admin_id = row[0]

    # Remove existing cookie for this admin if it exists
    delete_query = "DELETE FROM cookies WHERE admin_id = %s"
    cursor.execute(delete_query, (admin_id,))

    # Generate a random cookie value
    cookie = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)
    query = """
        INSERT INTO cookies (admin_id, cookie, expires_at)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (admin_id, cookie, expires_at))
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"cookie": cookie, "expires_at": expires_at.isoformat()}

@app.post("/cookies/check")
async def check_cookie(email_address: str, cookie: str):
    mydb = connect_to_db()
    cursor = mydb.cursor()

    # Look up admin_id by email address
    cursor.execute("SELECT admin_id FROM administrators WHERE email_address = %s", (email_address,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail="Email address not found")
    admin_id = row[0]

    query = "SELECT expires_at FROM cookies WHERE admin_id = %s AND cookie = %s"
    cursor.execute(query, (admin_id, cookie))
    result = cursor.fetchone()

    if result is None:
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=404, detail="Invalid cookie or admin ID")
    expires_at = result[0]  # Now this is always expires_at

    # Convert expires_at to datetime if it's a string
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)

    if datetime.utcnow() > expires_at:
        # Remove the cookie
        delete_query = "DELETE FROM cookies WHERE admin_id = %s AND cookie = %s"
        cursor.execute(delete_query, (admin_id, cookie))
        mydb.commit()
        cursor.close()
        mydb.close()
        raise HTTPException(status_code=403, detail="Cookie has expired")
    cursor.close()
    mydb.close()
    return {"message": "Cookie is valid", "expires_at": expires_at.isoformat()}