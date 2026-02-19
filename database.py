import asyncpg

# Database connection pool
db_pool = None

async def init_db():
    """Initialize database connection pool"""
    global db_pool
    db_pool = await asyncpg.create_pool(
        host="localhost",
        database="quick_links",
        user="shafalisingh",  
        password="",
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