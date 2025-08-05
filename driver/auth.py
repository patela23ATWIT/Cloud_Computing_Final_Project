import httpx
import getpass
import asyncio

_saved_email = None
_saved_cookie = None
COOKIES_ISSUE_URL = "http://localhost:8007/cookies/issue"

def save_cookie_var(email: str, cookie: str):
    global _saved_email, _saved_cookie
    _saved_email = email
    _saved_cookie = cookie
    
def get_saved_cookie():
    global _saved_email, _saved_cookie
    if _saved_email is None or _saved_cookie is None:
        asyncio.run(prompt_and_get_new_cookie())
    return _saved_email, _saved_cookie

async def get_new_cookie(email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            COOKIES_ISSUE_URL,
            json={"email_address": email, "password": password}  # <-- changed to json# <-- changed to json
        )
        if response.status_code != 200:
            raise Exception("Failed to issue cookie")
        cookie = response.json().get("cookie")
        print(f"Issued new cookie: {cookie}")
        save_cookie_var(email, cookie)

async def prompt_and_get_new_cookie():
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    return await get_new_cookie(email, password)


def get_auth_headers():
    email, cookie = get_saved_cookie()
    return {
        "X-Email-Address": email,
        "X-Session-Cookie": cookie
    }