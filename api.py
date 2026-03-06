from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agents.coordinator import CoordinatorAgent
from agents.image_agent import ImageAgent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = CoordinatorAgent()
image_agent = ImageAgent()

class QueryRequest(BaseModel):
    topic: str

class ImageRequest(BaseModel):
    image_base64: str
    question: Optional[str] = "Describe this image in detail."

@app.post("/run")
def run_pipeline(req: QueryRequest):
    result = coordinator.execute(req.topic)
    return result

@app.post("/analyze-image")
def analyze_image(req: ImageRequest):
    result = image_agent.run(req.image_base64, req.question)
    return {"analysis": result}