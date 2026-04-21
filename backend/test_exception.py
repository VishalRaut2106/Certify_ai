#!/usr/bin/env python3
import asyncio
from app.api.v1.endpoints.certificates import get_user_certificates
from app.core.database import connect_to_mongo, close_mongo_connection

async def test():
    await connect_to_mongo()
    try:
        user = {"id": "bf7f0ba7-e7ca-4400-89df-53f62a7459e8"}
        res = await get_user_certificates(current_user=user, status_filter=None, limit=50, skip=0)
        print("Success:", res)
    except Exception as e:
        print("Error:", type(e).__name__, str(e))
        import traceback
        traceback.print_exc()
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(test())
