# ✅ Updated Flask App with LangChain v0.2+ Syntax & GPT-4 Integration + Home Route

from flask import Flask, request, jsonify
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os

app = Flask(__name__)

# Load your OpenAI API key (set your actual key here or through environment variables)
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Load PDF and extract content
loader = PyPDFLoader("ev_articles.pdf")
pages = loader.load()
text_data = "\n".join([p.page_content for p in pages])

# Setup LLM (GPT-4)
llm = ChatOpenAI(model="gpt-4")

# Prompt Template
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a business analyst AI. Analyze the following EV industry document and generate the following sections:

1. Executive Summary
2. Market Trends
3. Key Players & Competitor Analysis
4. SWOT or PESTEL Analysis
5. Strategic Recommendations
6. Sources & References

Document:
{text}
"""
)

# Chain using new Runnable style
chain = prompt | llm

@app.route('/')
def home():
    return """
    <h2>✅ Server is running!</h2>
    <p>Click below to generate the EV industry report:</p>
    <a href='/generate-report'>Generate Report</a>
    """

@app.route('/generate-report', methods=['GET'])
def generate_report():
    response = chain.invoke({"text": text_data[:10000]})
    return jsonify({"report": response})

if __name__ == '__main__':
    app.run(debug=True)
