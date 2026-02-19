from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from models import URLRequest
from database import init_db, close_db, create_short_url, get_long_url
from utils import encode_base36, decode_base36

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(lifespan=lifespan)

# Home Page
@app.get("/")
async def root():
    return {"message": "QuickLink API is running"}

# simple array db for now to store urls
url_db = []
next_id = 1


# Shorten the Url => POST
@app.post("/shorten")
async def shorten_url(request: URLRequest):
    url_id = await create_short_url(request.long_url)
    
    # Generate short code
    short_code = encode_base36(url_id)
    
    return {
        "short_code": short_code,
        "short_url": f"http://localhost:8000/{short_code}",
        "original_url": request.long_url
    }

    
@app.get("/{short_code}")
async def get_url(short_code: str):
    try:
        url_id = decode_base36(short_code)
    except:
        raise HTTPException(status_code=404, detail="Invalid short code")
    
    # Get URL from database
    long_url = await get_long_url(url_id)
    
    if long_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=long_url)

        

@app.get("/debug/db-test")
async def test_db():
    try:
        query = "SELECT COUNT(*) as count FROM urls"
        async with db_pool.acquire() as connection:
            row = await connection.fetchrow(query)
            return {"status": "connected", "total_urls": row['count']}
    except Exception as e:
        return {"status": "error", "message": str(e)}