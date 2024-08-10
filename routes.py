from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from utils import QueueHandler, retrieve_results

content_router = APIRouter()

class Message(BaseModel):
    session_id: str
    topic: str

# Request body models
class ContentRequest(BaseModel):
    messages: List[Message]
    
    
# Invoke the topics to SQS Queue   
@content_router.post("/upload-topics")
async def upload_topics(body: ContentRequest):
    response = QueueHandler(body.messages)
    return {"code": 200, "message": "Response successfully generated.", "response": response, "metadata": {}}


# Retrive the generated results   
@content_router.post("/result")
async def get_result(session_id: str):
    result = retrieve_results(session_id)
    return {"code": 200, "message": "Response successfully generated.", "response": result, "metadata": {}}
