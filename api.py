from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os


app= FastAPI(
    title="RAG_Chat_Bot",
    version="v1",
    description="Feedback intelligence system with JWT authentication"
)


@app.get("/we up gng?")
async def health():
    return {"status": "everything is gooddd"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


