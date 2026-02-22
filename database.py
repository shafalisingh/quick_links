import asyncpg
import os
# Database connection pool
db_pool = None


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

async def close_db():
    """Close database connection pool"""
    if db_pool:
        await db_pool.close()

async def create_short_url(long_url: str) -> int:
    """Insert URL into database and return the ID"""
    query = "INSERT INTO urls (long_url) VALUES ($1) RETURNING id"
    async with db_pool.acquire() as connection:
        row = await connection.fetchrow(query, long_url)
        return row['id']

async def get_long_url(url_id: int) -> str:
    """Get original URL by ID"""
    query = "SELECT long_url FROM urls WHERE id = $1"
    async with db_pool.acquire() as connection:
        row = await connection.fetchrow(query, url_id)
        return row['long_url'] if row else None
    
async def record_click(url_id: int, ip_address: str = None, user_agent: str = None):
    """Record a click in the database"""
    query = """
        INSERT INTO clicks (url_id, ip_address, user_agent) 
        VALUES ($1, $2, $3)
    """
    async with db_pool.acquire() as connection:
        await connection.execute(query, url_id, ip_address, user_agent)