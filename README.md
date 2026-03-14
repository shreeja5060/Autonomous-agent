# 🤖 Autonomous Agent Pro

> A production-grade multi-agent AI system that researches, teaches, writes code, analyzes images, and learns from your feedback.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange)
![Docker](https://img.shields.io/badge/Docker-Hub-blue)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Live Demo
**API:** https://autonomous-agent-38cl.onrender.com/docs
**Frontend:** https://shreeja5060.github.io/Autonomous-agent/frontend.html
**Docker Hub:** https://hub.docker.com/r/shreeja5060/autonomous-agent
**GitHub:** https://github.com/shreeja5060/Autonomous-agent

> ⚠️ First request may take 30-60 seconds — free tier server sleeps when inactive.

---

## 🚀 What This Project Does

This is not a simple chatbot. It is a **multi-agent AI pipeline** where specialized agents work together in sequence to produce high quality, evaluated responses — with real web search, image understanding, and a reinforcement learning feedback loop.

You type a question. The system figures out what you need, routes it to the right agents, searches the web for live data, generates a response, scores it, and learns from your rating.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| **Multi-Agent Pipeline** | 7 specialized agents working in sequence |
| **Intent Detection** | Automatically detects if you want research, teaching, code, or comparison |
| **Real Web Search** | ResearchAgent searches DuckDuckGo for live, current data — not just model memory |
| **Image Analysis** | Upload any image and ask questions about it using a vision model |
| **Vector Memory** | ChromaDB semantic search — finds similar past research not just exact matches |
| **Self Evaluation** | CriticAgent scores every response 0-10 with strengths and improvements |
| **RL Feedback Loop** | Rate responses 1-5 stars — ratings are saved and used to improve future responses |
| **REST API** | Full FastAPI backend with auto-generated docs at `/docs` |
| **Browser Frontend** | Clean dark UI — no installation needed, just open the HTML file |
| **Docker** | Containerized and published to Docker Hub — run with one command |
| **CI/CD** | GitHub Actions runs tests automatically on every push |

---

## 🏗️ Architecture
```
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│           CoordinatorAgent              │
│   Detects intent → plans pipeline       │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
  ┌────▼─────┐    ┌─────▼──────┐
  │ Research │    │   Teach    │
  │  Agent   │    │   Agent    │
  └────┬─────┘    └─────┬──────┘
       │                │
  ┌────▼─────┐    ┌─────▼──────┐
  │ Summary  │    │    Code    │
  │  Agent   │    │   Agent    │
  └────┬─────┘    └─────┬──────┘
       │                │
  ┌────▼─────┐    └─────┬──────┘
  │Comparison│          │
  │  Agent   │          │
  └────┬─────┘          │
       └───────┬─────────┘
               │
    ┌──────────▼──────────┐
    │     CriticAgent     │
    │  Scores 0-10        │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   ChromaDB Vector   │
    │   Semantic Memory   │
    └─────────────────────┘
               │
    ┌──────────▼──────────┐
    │    RL Feedback      │
    │  User rates 1-5 ★   │
    └─────────────────────┘
```

---

## 🐳 Docker

Pull and run with one command — no cloning or building required:
```bash
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_groq_key \
  shreeja5060/autonomous-agent
```

Then open: http://localhost:8000/docs

Get your free Groq API key at https://console.groq.com

Verified cross-platform on Windows and MacOS.

---

## 📊 Benchmarks

Tested across 5 diverse research queries on local environment.

| Metric | Result |
|--------|--------|
| Queries Tested | 5 |
| Average Response Time | 4.72 seconds |
| Average Quality Score | 8.0 / 10 |
| Fastest Response | 2.43 seconds |
| Slowest Response | 6.31 seconds |
| Evaluation Method | LLM-as-judge (CriticAgent) |
| Human Feedback | Star ratings (1-5) via RLHF loop |
| Models Evaluated | LLaMA 3.3 70B + LLaMA 4 Scout |

| Query | Score | Latency |
|-------|-------|---------|
| What is machine learning | 8.0/10 | 6.20s |
| What is quantum computing | 8.0/10 | 3.88s |
| What is blockchain | 8.0/10 | 6.31s |
| What is reinforcement learning | 8.0/10 | 4.79s |
| What is computer vision | 8.0/10 | 2.43s |

> ⚠️ Live deployment on Render free tier may have higher latency on first request due to server cold start (30-60 seconds). Subsequent requests perform similarly to local benchmarks.

---

## 🧠 Design Decisions

**Why DuckDuckGo over Google Search?**
DuckDuckGo's `ddgs` library requires no API key, has no rate limit for small usage, and returns clean structured results. Google Custom Search costs money and has a 100 query/day free limit. For a portfolio project DuckDuckGo is the right tradeoff.

**Why max_tokens=10 for intent detection?**
Intent detection only needs one word back — research, teaching, coding, or comparison. Setting max_tokens=10 makes the call 60x faster and cheaper than a standard 600 token call. Speed matters when this runs on every single query.

**Why 2 iterations not 3?**
Each iteration costs 3 API calls and 10-15 seconds. After 2 iterations the quality improvement is marginal — the critic scores rarely change significantly on a third attempt. 2 gives the retry benefit without tripling latency.

**Why does CriticAgent return a dict instead of a string?**
The coordinator needs to programmatically read `should_retry` and `overall_score` to make routing decisions. A string cannot be parsed reliably. A dictionary gives direct key access — `evaluation["should_retry"]` — which is safe and predictable.

**Why separate agents instead of one big prompt?**
Single responsibility makes each agent easier to debug, test, and improve independently. If the summary quality drops you fix SummaryAgent without touching ResearchAgent. This mirrors microservices architecture in production systems.

**Why strict scoring in CriticAgent?**
Original implementation had leniency bias — LLMs tend to score 7-9 regardless of actual quality. Fixed by adding explicit scoring guidelines: average responses score 5-6, only exceptional responses get 8+. This makes should_retry actually trigger on poor quality responses.

**Why ChromaDB over JSON memory?**
JSON memory only matches exact topic strings — "AI healthcare" would not match "AI in medicine." ChromaDB uses vector embeddings and cosine similarity to find semantically similar past research. This means the agent recalls relevant context even when the query is phrased differently.

---

## 🤖 Agent Descriptions

### 1. CoordinatorAgent
The brain of the system. Reads your query and decides which pipeline to run. Uses the LLM to classify intent into: `research`, `teaching`, `coding`, or `comparison`. Routes to the right agents automatically.

### 2. ResearchAgent
Searches DuckDuckGo for real, live web results. Passes those results to the LLM which reasons over actual current data — not outdated training memory. Also checks ChromaDB vector memory for semantically similar past research and builds on it.

### 3. SummaryAgent
Takes raw research output and condenses it into a clear, structured, actionable executive summary. Focuses on key takeaways and practical insights.

### 4. TeachAgent
Activated when you ask to learn something. Structures the response as: simple explanation → real world analogy → step by step breakdown → code example → common mistakes. Designed for genuine understanding.

### 5. CodeAgent
Activated when you ask for code. Writes clean, commented, working code with explanation, example usage, and edge case notes.

### 6. ComparisonAgent
Activated when you ask to compare two things. Returns structured side by side analysis with overview, similarities, differences, when to use each, and final recommendation.

### 7. ImageAgent
Uses a multimodal vision model (`meta-llama/llama-4-scout-17b-16e-instruct`) to analyze uploaded images. You can upload any image, ask a question about it, and get a detailed analysis.

### 8. CriticAgent
Evaluates every response on completeness, accuracy, clarity, and usefulness. Returns a score out of 10, a list of strengths, and specific improvements. Uses strict scoring guidelines to avoid leniency bias. Can trigger a retry if quality is too low.

---

## 🧠 Reinforcement Learning Feedback Loop

After every response, you can rate it 1-5 stars with an optional comment.
```
User rates response → saved to feedback.json
                   → average rating tracked
                   → high quality responses identified
                   → low quality responses flagged
```

This creates a dataset of what good and bad responses look like for your specific use cases — the foundation for fine-tuning or prompt optimization over time.

---

## 💾 Vector Memory (ChromaDB)

Every query and response is saved to a ChromaDB vector database. When you ask about a similar topic again, the ResearchAgent uses semantic search to find relevant past research — not just exact keyword matching.
```
First query:  "AI in healthcare"     → saved to ChromaDB
Second query: "AI in medicine"       → semantic search finds
                                       "AI in healthcare" match
                                     → builds on past research
```

Memory persists across server restarts.

---

## 📁 Project Structure
```
autonomous_agent/
├── agents/
│   ├── coordinator.py       # Intent detection + pipeline routing
│   ├── research_agent.py    # Web search + LLM reasoning
│   ├── summary_agent.py     # Condenses research
│   ├── teach_agent.py       # Step-by-step teaching
│   ├── code_agent.py        # Code generation
│   ├── comparison_agent.py  # Side by side comparison
│   ├── critic_agent.py      # Quality evaluation
│   └── image_agent.py       # Vision model analysis
├── memory/
│   ├── vector_memory.py     # ChromaDB semantic memory
│   ├── memory_store.py      # Original JSON memory (kept for reference)
│   └── feedback_store.py    # RL feedback storage
├── tests/
│   └── test_agents.py       # Unit tests with pytest
├── .github/
│   └── workflows/
│       └── deploy.yml       # GitHub Actions CI/CD
├── pipelines/
│   └── task_pipeline.py     # Original pipeline
├── chroma_db/               # Auto-generated vector database
├── api.py                   # FastAPI backend
├── frontend.html            # Browser UI
├── Dockerfile               # Docker container config
├── .dockerignore            # Docker ignore rules
├── app.py                   # Original CLI entry point
├── feedback.json            # Auto-generated feedback store
├── requirements.txt
└── .env                     # Your API keys (never commit this)
```

---

## ⚡ Quick Start

### Option 1 — Docker (recommended)
```bash
docker run -p 8000:8000 \
  -e GROQ_API_KEY=your_key \
  shreeja5060/autonomous-agent
```

### Option 2 — Local

#### 1. Clone the repo
```bash
git clone https://github.com/shreeja5060/Autonomous-agent.git
cd Autonomous-agent
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Set up environment
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at [console.groq.com](https://console.groq.com)

#### 4. Start the backend
```bash
uvicorn api:app --reload
```

#### 5. Open the frontend
Double click `frontend.html` → open with Chrome

---

## 🧪 Testing

Run unit tests locally:
```bash
pip install pytest
pytest tests/
```

CI/CD runs automatically on every push via GitHub Actions.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Project info and status |
| `POST` | `/run` | Run the full agent pipeline |
| `POST` | `/analyze-image` | Analyze an uploaded image |
| `POST` | `/feedback` | Submit a star rating |
| `GET` | `/feedback/stats` | Get RL learning statistics |
| `GET` | `/metrics` | Get system metrics |

### Example request
```bash
curl -X POST https://autonomous-agent-38cl.onrender.com/run \
  -H "Content-Type: application/json" \
  -d '{"topic": "explain transformers in AI"}'
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq API — LLaMA 3.3 70B |
| Vision | Groq — LLaMA 4 Scout (multimodal) |
| Web Search | DuckDuckGo Search (ddgs) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Vector Memory | ChromaDB (semantic search) |
| RL Feedback | JSON file store + stats tracking |
| Deployment | Render (auto-deploy from GitHub) |
| Container | Docker — published to Docker Hub |
| CI/CD | GitHub Actions — auto test on push |
| Testing | pytest |

---

## 🛣️ Roadmap

- [x] Multi-agent pipeline
- [x] Self evaluation with critic
- [x] FastAPI backend
- [x] Episodic memory
- [x] Real web search
- [x] Intent detection
- [x] Image analysis
- [x] RL feedback loop
- [x] Live deployment on Render
- [x] Docker containerization
- [x] Published to Docker Hub
- [x] ComparisonAgent
- [x] Unit tests with pytest
- [x] CI/CD with GitHub Actions
- [x] Leniency bias fixed
- [x] Vector database memory (ChromaDB)
- [ ] Async pipeline
- [ ] AWS migration
- [ ] Fine-tuning pipeline

---

## 📄 License

MIT © Shreeja 2026