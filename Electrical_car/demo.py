# 📦 Fully-Automated Industry Intelligence Report Generator

# Step-by-step code for each component

# Step 1: User Input Handler (FastAPI)
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/generate_report")
async def generate_report(query: Query):
    result = process_pipeline(query.question)
    return {"report_html": result}

# Step 2: Task Orchestrator
from modules.research import get_market_data
from modules.analysis import analyze_data
from modules.writer import create_report

def process_pipeline(query):
    raw_data = get_market_data(query)
    analysis = analyze_data(query, raw_data)
    final_report = create_report(analysis)
    return final_report

# modules/research.py
# Step 3: Data Fetcher (using SerpAPI)
import os
from serpapi import GoogleSearch

def get_market_data(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY")
    }
    search = GoogleSearch(params)
    results = search.get("organic_results", [])
    text_data = "\n".join([r["snippet"] for r in results if "snippet" in r])
    return text_data

# modules/analysis.py
# Step 4: NLP Analyzer (GPT-based)
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4")

def analyze_data(query, content):
    prompt = f"""
    You are a market analyst. Based on this data:
    ===\n{content}\n===
    Generate:
    1. Executive Summary
    2. Market Overview
    3. Top 3 Competitors with SWOT
    4. 3 Strategic Recommendations
    """
    response = llm.predict(prompt)
    return response

# modules/writer.py
# Step 5: Report Generator using HTML Template
from jinja2 import Template

html_template = """
<html>
<head><title>Industry Intelligence Report</title></head>
<body>
<h1>Industry Intelligence Report</h1>
<pre>{{ report_text }}</pre>
</body>
</html>
"""

def create_report(report_text):
    template = Template(html_template)
    return template.render(report_text=report_text)

# Step 6: Run FastAPI App
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# ✅ To test:
# Send POST request to http://localhost:8000/generate_report
# Body: { "question": "Generate a strategic report on the electric vehicle market and its key players" }
