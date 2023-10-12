from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Tuple
import uuid


# class Message(BaseModel):
#     id = uuid.uuid4()
#     msg: str
#     timestamp = str(datetime.now())


class Chat(BaseModel):
    user_id: str
    token: str
    history: List[Tuple[str, str]]
    title: Optional[str] = None
    session_start: str = str(datetime.now())

class User(BaseModel):
    user_id: str = str(uuid.uuid4())
    email: str
    password: str
    created_at: str = str(datetime.now())