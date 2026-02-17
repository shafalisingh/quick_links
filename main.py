from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

class URLRequest(BaseModel):
    long_url: str
    
app = FastAPI()

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
    global next_id
    original_url = request.long_url
    
    url_db.append({
        "id": next_id,
        "long_url": original_url
    })
    
    short_code = encode_base36(next_id)
    next_id += 1
    
    
    
    return {
        "short_code": short_code,
        "short_url": f"http://localhost:8000/{short_code}",
        "original_url": original_url, 
        "url_db": url_db
    }
    
@app.get("/{short_code}")
async def get_url(short_code: str):
    try:
        url_id = decode_base36(short_code)
    except:
        raise HTTPException(status_code=404, detail="Invalid short code")
    
    for entry in url_db:
        if entry["id"] == url_id:
            # Found it! Redirect to the long URL
            return RedirectResponse(url=entry["long_url"])
    raise HTTPException(status_code=404, detail="URL not found")

        

def encode_base36(num: int) -> str:
    """Convert a number to base36 string"""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    if num == 0:
        return alphabet[0]
    
    result = ""
    while num > 0:
        remainder = num % 36
        result = alphabet[remainder] + result
        num = num // 36
    
    return result

def decode_base36(code: str) -> int:
    """Convert a base36 string back to a number"""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    result = 0
    for char in code:
        result = result * 36 + alphabet.index(char)
    
    return result