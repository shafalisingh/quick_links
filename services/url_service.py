async def get_url_analytics(url_id: int):
        async with db_pool.acquire() as connection:
            
            url_row = await connection.fetchrow(
                "SELECT long_url, created_at FROM urls WHERE id = $1",
                url_id
            )

            if url_row is None:
                return None

            count_row = await connection.fetchrow(
                "SELECT COUNT(*) as total FROM clicks WHERE url_id = $1",
                url_id
            )

            recent_clicks = await connection.fetch(
                """
                SELECT clicked_at
                FROM clicks
                WHERE url_id = $1
                ORDER BY clicked_at DESC
                LIMIT 10
                """,
                url_id
            )

            return {
                "long_url": url_row["long_url"],
                "created_at": str(url_row["created_at"]),
                "total_clicks": count_row["total"],
                "recent_clicks": [
                    {"clicked_at": str(click["clicked_at"])}
                    for click in recent_clicks
                ]
            }