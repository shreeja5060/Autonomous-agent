# 🤖 Autonomous Agent Pro

> A production-grade multi-agent AI system that researches, teaches, writes code, analyzes images, and learns from your feedback.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 What This Project Does

This is not a simple chatbot. It is a **multi-agent AI pipeline** where specialized agents work together in sequence to produce high quality, evaluated responses — with real web search, image understanding, and a reinforcement learning feedback loop.

You type a question. The system figures out what you need, routes it to the right agents, searches the web for live data, generates a response, scores it, and learns from your rating.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| **Multi-Agent Pipeline** | 6 specialized agents working in sequence |
| **Intent Detection** | Automatically detects if you want research, teaching, code, or comparison |
| **Real Web Search** | ResearchAgent searches DuckDuckGo for live, current data — not just model memory |
| **Image Analysis** | Upload any image and ask questions about it using a vision model |
| **Episodic Memory** | Remembers past conversations and builds on them across sessions |
| **Self Evaluation** | CriticAgent scores every response 0-10 with strengths and improvements |
| **RL Feedback Loop** | Rate responses 1-5 stars — ratings are saved and used to improve future responses |
| **REST API** | Full FastAPI backend with auto-generated docs at `/docs` |
| **Browser Frontend** | Clean dark UI — no installation needed, just open the HTML file |

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
  │(web search│    │(step by   │
  │+ LLM)    │    │ step)      │
  └────┬─────┘    └─────┬──────┘
       │                │
  ┌────▼─────┐    ┌─────▼──────┐
  │ Summary  │    │    Code    │
  │  Agent   │    │   Agent    │
  └────┬─────┘    └─────┬──────┘
       │                │
       └───────┬─────────┘
               │
    ┌──────────▼──────────┐
    │     CriticAgent     │
    │  Scores 0-10        │
    │  Strengths +        │
    │  Improvements       │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
    │   EpisodicMemory    │
    │   Saves to disk     │
    │   Builds context    │
    └─────────────────────┘
               │
    ┌──────────▼──────────┐
    │    RL Feedback      │
    │  User rates 1-5 ★   │
    │  Saved to           │
    │  feedback.json      │
    └─────────────────────┘
```

---

## 🤖 Agent Descriptions

### 1. CoordinatorAgent
The brain of the system. Reads your query and decides which pipeline to run. Uses the LLM to classify intent into: `research`, `teaching`, `coding`, or `comparison`. Routes to the right agents automatically.

### 2. ResearchAgent
Searches DuckDuckGo for real, live web results. Passes those results to the LLM which reasons over actual current data — not outdated training memory. Also checks episodic memory for past context on the same topic and builds on it.

### 3. SummaryAgent
Takes raw research output and condenses it into a clear, structured, actionable executive summary. Focuses on key takeaways and practical insights.

### 4. TeachAgent
Activated when you ask to learn something. Structures the response as: simple explanation → real world analogy → step by step breakdown → code example → common mistakes. Designed for genuine understanding.

### 5. CodeAgent
Activated when you ask for code. Writes clean, commented, working code with explanation, example usage, and edge case notes.

### 6. ImageAgent
Uses a multimodal vision model (`meta-llama/llama-4-scout-17b-16e-instruct`) to analyze uploaded images. You can upload any image, ask a question about it, and get a detailed analysis.

### 7. CriticAgent
Evaluates every response on completeness, accuracy, clarity, and usefulness. Returns a score out of 10, a list of strengths, and specific improvements. Can trigger a retry if quality is too low.

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

## 💾 Episodic Memory

Every query and response is saved to `memory.json` per topic. When you ask about the same topic again, the ResearchAgent loads the previous context and builds on it rather than starting from scratch.

```
First query:  "AI in healthcare"  → researches from scratch → saved
Second query: "AI in healthcare"  → loads memory → goes deeper
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
│   ├── critic_agent.py      # Quality evaluation
│   └── image_agent.py       # Vision model analysis
├── memory/
│   ├── memory_store.py      # Episodic memory (disk-backed)
│   └── feedback_store.py    # RL feedback storage
├── pipelines/
│   └── task_pipeline.py     # Original pipeline
├── api.py                   # FastAPI backend
├── frontend.html            # Browser UI
├── app.py                   # Original CLI entry point
├── memory.json              # Auto-generated memory store
├── feedback.json            # Auto-generated feedback store
├── requirements.txt
└── .env                     # Your API keys (never commit this)
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/shreeja5060/Autonomous-agent.git
cd Autonomous-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free API key at [console.groq.com](https://console.groq.com)

### 4. Start the backend
```bash
uvicorn api:app --reload
```
API runs at `http://127.0.0.1:8000`
Auto-generated docs at `http://127.0.0.1:8000/docs`

### 5. Open the frontend
Double click `frontend.html` → open with Chrome

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/run` | Run the full agent pipeline |
| `POST` | `/analyze-image` | Analyze an uploaded image |
| `POST` | `/feedback` | Submit a star rating |
| `GET` | `/feedback/stats` | Get RL learning statistics |

### Example request
```bash
curl -X POST http://127.0.0.1:8000/run \
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
| Memory | JSON file store (disk-backed) |
| RL Feedback | JSON file store + stats tracking |

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
- [ ] Docker containerization
- [ ] CI/CD with GitHub Actions
- [ ] Cloud deployment

---

## 📄 License

MIT © Shreeja 2025
