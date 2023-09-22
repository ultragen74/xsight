from fastapi import WebSocket, status, Query
from typing import Optional
from redis_setup.config import Redis
from pymongo import MongoClient
client=MongoClient()

async def get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):

    if token is None or token == "":
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    print("token found", token)
    redis_obj = Redis()

    redis_client = await redis_obj.create_connection()
    isexists = await redis_client.exists(token)
    with MongoClient() as client:
        chat_collection = client["chat"]["chat_collection"]
        rows = chat_collection.find({"token": token})
        for row in rows:
            isexists = 1

    if isexists == 1:
        print("returning token")
        return token
    else:
        print("exception")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Session not authenticated or expired token")