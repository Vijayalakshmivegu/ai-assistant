# AI Research Assistant ⚡

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.x-lightgrey.svg)](https://flask.palletsprojects.com/)

Real-time AI assistant combining Ollama LLMs with Tavily search for lightning-fast research.

## Features
- Dual-model architecture (`llama3:8b` + `phi3`)
- Tavily API integration for live data
- Full chat history with Flask backend
- Optimized for <1.5s responses

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure `.env`:
   ```ini
   TAVILY_API_KEY=your_key
   OLLAMA_HOST=http://localhost:11434
   ```
3. Run:
   ```bash
   python app.py
   ```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/new_chat` | POST | Creates new chat |
| `/api/chat/<id>` | POST | Processes message |
| `/api/chats` | GET | Lists all chats |

![Architecture Diagram](/static/architecture.png)
