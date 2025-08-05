import httpx
from fastapi import HTTPException
from fastapi import Depends, Request

COOKIES_SERVICE_URL = "http://localhost:8007/cookies/check"
COOKIES_ISSUE_URL = "http://localhost:8007/cookies/issue"


async def verify_cookie(email: str, cookie: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            COOKIES_SERVICE_URL,
            params={"email_address": email, "cookie": cookie}
        )
        if response.status_code != 200:
            raise False
        return True

async def issue_cookie(email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            COOKIES_ISSUE_URL,
            params={"email_address": email, "password": password}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to issue cookie")
        return response.json()
