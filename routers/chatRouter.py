import os

from fastapi import APIRouter
from openai import OpenAI

import config
from schemes.chatSchemes import ChatResponse, ChatRequest

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

client = OpenAI(api_key=config.OPENAI_API_KEY)

@router.post("", response_model=ChatResponse)
def get_chat(request: ChatRequest):
    completion = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=[{"role":"user","content": request.message}],
    )

    response_text = completion.choices[0].message.content
    return ChatResponse(response=response_text)