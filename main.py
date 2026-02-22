from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from contextlib import asynccontextmanager 
from models import URLRequest
from database import init_db, close_db, create_short_url, get_long_url, record_click
from utils import encode_base36, decode_base36
from services.url_service import get_url_analytics

import asyncpg
import os
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
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
    url_id = await create_short_url(str(request.long_url))
    
    # Generate short code
    short_code = encode_base36(url_id)
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    
    return {
        "short_code": short_code,
        "short_url": f"{BASE_URL}/{short_code}",
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
    asyncio.create_task(record_click(url_id))
    return RedirectResponse(url=long_url)



@app.get("/analytics/{short_code}")

async def get_analytics(short_code: str):
    
    try:
        url_id = decode_base36(short_code)
    except:
        raise HTTPException(status_code=404, detail="Invalid short code")
    
    analytics = await get_url_analytics(url_id)
    
    if not analytics:
        raise HTTPException(status_code=404, detail="URL not found")
    return analytics