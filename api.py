from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
from models import SubmitQuery
from client import generate_answer
from schema import Answer
app= FastAPI(
    title="RAG_Chat_Bot",
    version="v1",
    description="making a rag chatbot to help users"
)

@app.post("/ask", response_model=Answer)
async def create_query(req : SubmitQuery):
    result = generate_answer(req.text)
    return result



@app.get("/we-up")
async def health():
    return {"status": "everything is gooddd"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


