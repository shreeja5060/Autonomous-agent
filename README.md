# Multi-Agent AI System

An autonomous AI system that researches topics, generates summaries, and evaluates its own output quality.

## Features
- Multi-agent architecture with coordinator, research, summary, and critic agents
- Self-evaluation scoring (0-10 scale)
- Automated quality metrics tracking
- Free to run using Groq API

## Quick Start

1. Install dependencies:
```bash
pip install groq python-dotenv
```

2. Create `.env` file with your Groq API key:
```
GROQ_API_KEY=your_key_here
```

3. Run:
```bash
python app.py
```

## Example Output
```
[ResearchAgent] Researching topic: AI in Healthcare
[SummaryAgent] Creating summary...
[CriticAgent] Evaluating quality...

Quality Score: 8.0/10
✅ Strengths: Clear overview, actionable insights
💡 Improvements: Add specific examples
```

## Tech Stack
- Python
- Groq API (Llama 3.3 70B)
- Multi-agent coordination system
```

**Save it.** That's it. Don't overthink it.

---

## **Step 2: Create requirements.txt (2 mins)**

Create `requirements.txt`:
```
groq>=1.0.0
python-dotenv>=1.0.0