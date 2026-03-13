from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from agents.coordinator import CoordinatorAgent
from agents.image_agent import ImageAgent
from memory.feedback_store import FeedbackStore

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Autonomous Multi-Agent AI System",
        "status": "running",
        "docs": "https://autonomous-agent-38cl.onrender.com/docs",
        "endpoints": ["/run", "/analyze-image", "/feedback", "/feedback/stats"]
    }

coordinator = CoordinatorAgent()
image_agent = ImageAgent()
feedback_store = FeedbackStore()

class QueryRequest(BaseModel):
    topic: str

class ImageRequest(BaseModel):
    image_base64: str
    question: Optional[str] = "Describe this image in detail."

class FeedbackRequest(BaseModel):
    topic: str
    response: str
    rating: int
    comment: Optional[str] = ""

@app.post("/run")
def run_pipeline(req: QueryRequest):
    result = coordinator.execute(req.topic)
    return result

@app.post("/analyze-image")
def analyze_image(req: ImageRequest):
    result = image_agent.run(req.image_base64, req.question)
    return {"analysis": result}

@app.post("/feedback")
def submit_feedback(req: FeedbackRequest):
    feedback_store.save_feedback(
        topic=req.topic,
        response=req.response,
        rating=req.rating,
        comment=req.comment
    )
    stats = feedback_store.get_stats()
    return {
        "status": "saved",
        "stats": stats
    }

@app.get("/feedback/stats")
def get_feedback_stats():
    return feedback_store.get_stats()