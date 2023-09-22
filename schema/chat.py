from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Tuple
import uuid


# class Message(BaseModel):
#     id = uuid.uuid4()
#     msg: str
#     timestamp = str(datetime.now())


class Chat(BaseModel):
    token: str
    history: List[Tuple[str, str]]
    name: str
    session_start: str = str(datetime.now())