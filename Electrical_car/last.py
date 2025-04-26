# ✅ Flask App with LangChain & GPT-4 + Professional Web Interface

from flask import Flask, request, render_template_string
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load OpenAI API key from environment variables
openai_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai_key

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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>EV Intelligence Report</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f9f9f9; margin: 0; padding: 0; }
        header { background: #004d99; color: white; padding: 1rem 0.5rem; text-align: center; }
        nav {
            background: #e6e6e6;
            padding: 0.75rem;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        nav a {
            text-decoration: none;
            margin: 0 1rem;
            font-weight: bold;
            color: #004d99;
        }
        main {
            max-width: 900px;
            margin: 2rem auto;
            background: white;
            padding: 2rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .btn {
            background: #004d99;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            cursor: pointer;
            font-size: 1rem;
        }
        section {
            margin-bottom: 2rem;
        }
        input[type="text"] {
            width: 100%;
            padding: 0.5rem;
            margin-bottom: 1rem;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        footer {
            background: #004d99;
            color: white;
            padding: 3rem;
            text-align: center;
            margin-top: 28rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>🔍 EV Industry Intelligence Report</h1>
    </header>
    <nav>
        <a href="/">Home</a>
        <a href="/generate-report">Generate Report</a>
    </nav>
    <main>
        {% if report %}
            <h2>📄 Generated Report</h2>
            {% for section in report.split('\n\n') %}
                <section>
                    <p>{{ section }}</p>
                </section>
            {% endfor %}
        {% else %}
            <h2>📘 Welcome</h2>
            <p>Enter your custom query below and generate your EV industry report.</p>
            <form action="/generate-report" method="post">
                <input type="text" name="query" placeholder="Enter your business query here..." required>
                <button class="btn" type="submit">Generate Report</button>
            </form>
        {% endif %}
    </main>
    <footer>
        &copy; 2025 Auto Report AI • All rights reserved
    </footer>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_TEMPLATE, report=None)

@app.route('/generate-report', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        user_query = request.form.get('query', '')
        if user_query:
            full_prompt = f"""You are a business analyst AI. {user_query}\n\nBased on the following document:\n{text_data[:10000]}"""
            response = llm.invoke(full_prompt)
        else:
            response = llm.invoke(text_data[:10000])
    else:
        response = chain.invoke({"text": text_data[:10000]})

    report_text = response.content if hasattr(response, 'content') else str(response)
    return render_template_string(HTML_TEMPLATE, report=report_text)

if __name__ == '__main__':
    app.run(debug=True)