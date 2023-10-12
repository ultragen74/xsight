from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
os.environ["REDIS_HOST"] = "127.0.0.1"
from dotenv import load_dotenv
from routes.chat import chat
from redis_setup.config import Redis
import asyncio
from starlette.middleware.sessions import SessionMiddleware



async def main():
    redis = Redis()
    redis = await redis.create_connection()
    print(redis)
    await redis.set("key", "value")

load_dotenv()


api = FastAPI()
api.include_router(chat)
api.mount("/static", StaticFiles(directory="static"), name="static")
api.add_middleware(SessionMiddleware, secret_key="3LYUDAJCWMYXV4Y359VVVM0EJPDHTOTBH8GW")

@api.get("/test")
async def root():
    return {"msg": "API is Online"}


if __name__ == "__main__":
    if os.environ.get('APP_ENV') == "development":
        asyncio.run(main())
        uvicorn.run("main:api", host="0.0.0.0", port=80,
                    workers=4, reload=True)
    else:
      pass
