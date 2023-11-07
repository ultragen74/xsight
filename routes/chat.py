import sys
sys.path.append("..")
import os
from fastapi import APIRouter, FastAPI, WebSocket,  Request, BackgroundTasks, HTTPException, WebSocketDisconnect, Depends, Form
import uuid
import json
from sockets.connection import ConnectionManager
from sockets.utils import get_token
from rejson import Path
import requests
from redis_setup.producer import Producer
from redis_setup.config import Redis
from schema.chat import Chat, User
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from redis_setup.cache import Cache
from langchain.memory import ConversationBufferMemory
from xsight.openai_chatbot import agent
print("will load model now")
# from xsight.chatbot import generate_response
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
async def token_generator(user_id: str):
    print("in token endpoint")
    token = str(uuid.uuid4())
    with MongoClient() as client:
      user_collection = client["chat"]["user_collection"]
      user = user_collection.find_one({"user_id": user_id})
    
    if not user:
        raise HTTPException(status_code=400, detail={
            "loc": "user_id",  "msg": "Enter a valid user_id"})

    # Create new chat session
    # json_client = redis.create_rejson_connection()
    with MongoClient() as client:
      chat_collection = client["chat"]["chat_collection"]
      chat = chat_collection.find_one({"user_id": user_id, "history": []})
    if chat:
        del chat["_id"]
        chat_session = Chat(**chat)
    else:
        chat_session = Chat(
            token=token,
            history=[],
            user_id=user_id
        )

        # Store chat session in redis JSON with the token as key
        # print(str(token), Path.rootPath(), json.dumps(chat_session.dict()))
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

@chat.get("/", response_class=HTMLResponse)
async def login(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse("/chat_ui", status_code=302)
    return templates.TemplateResponse("login.html",{"request": request})

@chat.get("/dashboard", response_class=HTMLResponse)
async def login(request: Request):
    if request.session.get("user_id"):
        return templates.TemplateResponse("dashboard.html",{"request": request})
    return RedirectResponse("/", status_code=302)


@chat.post("/", response_class=HTMLResponse)
async def login_redirect(request: Request, email: str = Form(...), password: str = Form(...)):
    # context = {"request": request}
    with MongoClient() as client:
        user_collection = client["chat"]["user_collection"]
        user = user_collection.find_one({"email": email})
    print(user)
    if not user:
        user = User(
            email=email,
            password=password
        )
        with MongoClient() as client:
            user_collection = client["chat"]["user_collection"]
            result = user_collection.insert_one(user.model_dump())
    request.session["email"] = email
    request.session["user_id"] = user["user_id"]
    return RedirectResponse("/chat_ui", status_code=302)

@chat.get("/chat_ui", response_class=HTMLResponse)
async def chat_ui(request: Request):
    print("request porcessing.")
    if request.session.get("user_id"):
        user_id = request.session["user_id"]
        context = {"request": request, "user_id": user_id}
        with MongoClient() as client:
            print("going for mongo")
            chat_collection = client["chat"]["chat_collection"]
            rows = chat_collection.find({"user_id": user_id})
            chat_data = []
            for data in rows:
                if data['history'] != []:
                    del data['_id']
                    print(data)
                    if 'title' in data:
                        for j in range(len(data['history'])):
                            usr_msg, ai_msg = data['history'][j]
                            data['history'][j] = [usr_msg.replace('\n', '<br>'), ai_msg.replace('\n', '<br>').replace('"', '\\"').replace('\\\"', '\\"')]
                        chat_data.append(data)
                else:
                    context["token"] = data['token']
        if "token" not in context:
            chat_session = Chat(
                token=str(uuid.uuid4()),
                history=[],
                user_id=user_id
            )

            # Store chat session in redis JSON with the token as key
            # print(str(token), Path.rootPath(), json.dumps(chat_session.dict()))
            with MongoClient() as client:
                chat_collection = client["chat"]["chat_collection"]
                result = chat_collection.insert_one(chat_session.model_dump())
            context['token'] = chat_session.token
        context["chats"] = chat_data
        print("template returned", context)
        return templates.TemplateResponse("index.html", context)
    return RedirectResponse("/", status_code=302)


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
                data = chat_collection.find_one({"token": token})
            # data = await cache.get_chat_history(token=token)
            # data = json.loads(data)
            stream_data = {}
            stream_data[token] = data
            msg_id = "mid"+str(uuid.uuid4())
            final_response = ""
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            agent.memory = memory
            history = data["history"]
            for usr_msg, ai_msg in history:
                agent.memory.chat_memory.add_user_message(usr_msg)
                agent.memory.chat_memory.add_ai_message(ai_msg)
            for resp in agent.run(user_msg["msg"]):
                f_resp = resp.replace('\n', '<br>').replace('"', '\\"')
                await manager.send_personal_message({'msg': f_resp, 'source': 'bot', 'id': msg_id}, websocket)
                final_response += f_resp
            history += [[user_msg["msg"], final_response]]
            
            # history = generate_response(user_msg["msg"], data["history"], table)
            # bot_msg = history[-1][1]
            data["history"] = history
            
            with MongoClient() as client:
                chat_collection = client["chat"]["chat_collection"]
                myquery = { "token": token}
                newvalues = { "$set": { "history": history, "title": history[0][0]} }

                chat_collection.update_one(myquery, newvalues)
            # json_client.jsonset(str(token), Path.rootPath(), json.dumps(data))
            # await producer.add_to_stream(stream_data, "message_channel")
            
            counter += 1

    except WebSocketDisconnect:
        manager.disconnect(websocket)