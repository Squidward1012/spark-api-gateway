from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel, validator
from dotenv import load_dotenv
from spark_chat import SparkChat
import os

load_dotenv()

app = FastAPI()

"""
{ 
    "messages": [ 
      { "role": "user", "content": "What is Large Language Model?" }
    ], 
    "temperature": 0.7, 
    "max_tokens": -1,
    "stream": false
  }
"""


class Message(BaseModel):
    role: str
    content: str


class ChatCompletion(BaseModel):
    temperature: float = 0.7
    max_tokens: Union[int, None]
    stream: bool = False
    messages: List[Message] = []
    model: str
    n: int

    @validator('max_tokens', pre=True, always=True)
    def set_max_tokens(cls, value):
        if value is None:
            return 2048
        return value

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/v1/chat/completions")
def chat_completion(chatCompletion: ChatCompletion):

    spark_chat = SparkChat(
        os.environ["APP_ID"],
        os.environ["API_KEY"],
        os.environ["API_SECRET"],
        "ws://spark-api.xf-yun.com/v1.1/chat",
        "general"
    )

    message_dicts = [{"role": msg.role, "content": msg.content} for msg in chatCompletion.messages]
    completion = spark_chat.chatCompletion(message_dicts, chatCompletion.temperature, chatCompletion.max_tokens)
    return completion
