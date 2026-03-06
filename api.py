from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.coordinator import CoordinatorAgent

app = FastAPI()

# This allows your HTML file to talk to your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = CoordinatorAgent()

class QueryRequest(BaseModel):
    topic: str

@app.post("/run")
def run_pipeline(req: QueryRequest):
    result = coordinator.execute(req.topic)
    return result