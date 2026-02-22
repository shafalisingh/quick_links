import asyncpg
from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    long_url: HttpUrl

async def save_url(pool, url_request: URLRequest):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO urls (long_url) VALUES ($1)",
            str(url_request.long_url)  # convert HttpUrl -> str
        )