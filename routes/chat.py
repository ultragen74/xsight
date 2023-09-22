import sys
sys.path.append("..")
import os
from fastapi import APIRouter, FastAPI, WebSocket,  Request, BackgroundTasks, HTTPException, WebSocketDisconnect, Depends
import uuid
import json
from sockets.connection import ConnectionManager
from sockets.utils import get_token
from rejson import Path
from redis_setup.producer import Producer
from redis_setup.config import Redis
from schema.chat import Chat
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from redis_setup.cache import Cache
from xsight.chatbot import generate_response
import pandas as pd
from pymongo import MongoClient
client=MongoClient()


templates = Jinja2Templates(directory="templates")


chat = APIRouter()
manager = ConnectionManager()
redis = Redis()
# @route   POST /token
# @desc    Route to generate chat token
# @access  Public
table = pd.read_csv("media/sales.csv")[:100]
@chat.post("/token")
async def token_generator(name: str, request: Request):
    token = str(uuid.uuid4())

    if name == "":
        raise HTTPException(status_code=400, detail={
            "loc": "name",  "msg": "Enter a valid name"})

    # Create new chat session
    json_client = redis.create_rejson_connection()

    chat_session = Chat(
        token=token,
        history=[],
        name=name
    )

    # Store chat session in redis JSON with the token as key
    print(str(token), Path.rootPath(), json.dumps(chat_session.dict()))
    with MongoClient() as client:
      chat_collection = client["chat"]["chat_collection"]
      result = chat_collection.insert_one(chat_session.model_dump())
    #   ack = result.acknowledged
    #   return {"insertion": ack}
    # json_client.jsonset(str(token), Path.rootPath(), json.dumps(chat_session.dict()))

    # Set a timeout for redis data
    redis_client = await redis.create_connection()
    # # await redis_client.expire(str(token), 3600)


    return chat_session.dict()


# @route   POST /refresh_token
# @desc    Route to refresh token
# @access  Public

@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None


@chat.get("/chat_ui", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("chat.html",{"request": request})


# @route   Websocket /chat
# @desc    Socket for chatbot
# @access  Public

@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket = WebSocket, token: str = Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    json_client = redis.create_rejson_connection()
    producer = Producer(redis_client)
    cache = Cache(json_client)
    counter = 1
    try:
        while True:
            data = await websocket.receive_text()
            user_msg = json.loads(data)
            print("data ->",user_msg["msg"], user_msg["source"])
            with MongoClient() as client:
                chat_collection = client["chat"]["chat_collection"]
                rows = chat_collection.find({"token": token})
                for data in rows:
                    break
            # data = await cache.get_chat_history(token=token)
            # data = json.loads(data)
            stream_data = {}
            stream_data[token] = data
            history = generate_response(user_msg["msg"], data["history"], table)
            bot_msg = history[-1][1]
            data["history"] = history
            with MongoClient() as client:
                chat_collection = client["chat"]["chat_collection"]
                myquery = { "token": token}
                newvalues = { "$set": { "history": history} }

                chat_collection.update_one(myquery, newvalues)
            # json_client.jsonset(str(token), Path.rootPath(), json.dumps(data))
            await producer.add_to_stream(stream_data, "message_channel")
            await manager.send_personal_message({"msg": bot_msg, "source": "bot"}, websocket)
            counter += 1

    except WebSocketDisconnect:
        manager.disconnect(websocket)