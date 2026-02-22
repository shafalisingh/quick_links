from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from contextlib import asynccontextmanager 
from models import URLRequest
from database import init_db, close_db, create_short_url, get_long_url, record_click
from utils import encode_base36, decode_base36
import asyncpg
import os
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

async def init_db():
    """Initialize database connection pool"""
    global db_pool
    
    # Use environment variable for Docker, fallback to localhost
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "quick_links")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "postgres")
    
    db_pool = await asyncpg.create_pool(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pass,
        min_size=1,
        max_size=10
    )

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/app")
async def serve_frontend():
    return FileResponse("static/index.html")
@app.get("/style.css")
async def serve_css():
    return FileResponse("static/style.css")

@app.get("/script.js")
async def serve_js():
    return FileResponse("static/script.js")
# Home Page

@app.get("/")
async def root():
    return {"message": "QuickLink API is running"}


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
    await record_click(url_id)
    return RedirectResponse(url=long_url)



@app.get("/analytics/{short_code}")

async def get_analytics(short_code: str):
    
    try:
        url_id = decode_base36(short_code)
    except:
        raise HTTPException(status_code=404, detail="Invalid short code")
    
    async with db_pool.acquire() as connection:
        # Get URL info
        url_query = "SELECT long_url, created_at FROM urls WHERE id = $1"
        url_row = await connection.fetchrow(url_query, url_id)
        
        if url_row is None:
            raise HTTPException(status_code=404, detail="URL not found")
        
        # Get click count
        count_query = "SELECT COUNT(*) as total FROM clicks WHERE url_id = $1"
        count_row = await connection.fetchrow(count_query, url_id)
        
        # Get recent clicks
        clicks_query = """
            SELECT clicked_at 
            FROM clicks 
            WHERE url_id = $1 
            ORDER BY clicked_at DESC 
            LIMIT 10
        """
        recent_clicks = await connection.fetch(clicks_query, url_id)
        
        return {
            "short_code": short_code,
            "long_url": url_row['long_url'],
            "created_at": str(url_row['created_at']),  # Convert to string
            "total_clicks": count_row['total'],
            "recent_clicks": [
                {
                    "clicked_at": str(click['clicked_at'])  # Convert to string
                }
                for click in recent_clicks
            ]
        }