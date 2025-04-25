# -*- coding: utf-8 -*-
import os
import time
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()
tavily_tool = TavilySearchResults(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=1,
    include_raw_content=True,
    timeout=1.2,
    search_depth="basic",  # Faster than "advanced"
    include_answer=True,  # Get direct answers when available
    include_images=False  # Skip images for speed
)
# Primary fast model (llama3:8b) and fallback ultra-fast model (phi3)
llm_fast = ChatOllama(
    model="llama3:8b",
    temperature=0.1,
    timeout=1.5,
    num_ctx=256
)
llm_ultrafast = ChatOllama(
    model="phi3",  # Smaller and faster than llama3
    temperature=0.1,
    timeout=0.8,  # Extremely fast
    num_ctx=128
)
def get_instant_answer(query: str) -> str:
    """Your existing get_instant_answer function"""
    start_time = time.time()
    try:
        result = tavily_tool.invoke({"query": query})[0]
        research_content = f"{result.get('title','')}: {result.get('content','')[:60]}"
    except:
        research_content = None

    try:
        if research_content:
            prompt = f"10-word answer about {query}: {research_content}"
            try:
                response = llm_ultrafast.invoke([HumanMessage(content=prompt)])
                if len(response.content.split()) <= 15:
                    return response.content
            except:
                pass
            response = llm_fast.invoke([HumanMessage(content=prompt)])
            return response.content
        
        fallback_answers = {
            "first ai model": "First AI: 1951 SNARC neural net (Minsky/Edmonds)",
            "latest ai": "Current leader: GPT-4 (2023)",
            "ai history": "AI began at 1956 Dartmouth workshop"
        }
        return fallback_answers.get(query.lower(), "Info unavailable. Try another question.")     
    except Exception as e:
        return f"Error: {str(e)}"
if __name__ == "__main__":
    print("⚡ Ultra-Fast AI Answers (Type 'exit' to quit)") 
    while True:
        try:
            query = input("\nAsk: ").strip().lower()
            if query in ["exit", "quit"]:
                break    
            print("⏳ Thinking...", end="\r", flush=True)
            start = time.time()
            response = get_instant_answer(query)
            elapsed = time.time() - start
            print(f"✅ Answer ({elapsed:.1f}s): {response}") 
        except KeyboardInterrupt:
            break
        except Exception:
            print("⚠️ Please try another question")