import requests
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import pipeline

class EVReportGenerator:
    def __init__(self, query):
        self.query = query
        self.logs = []  # new: store error/warning logs
        self.sources = []
        self.sections = {
            "Executive Summary": "",
            "Market Overview": "",
            "Key Trends": "",
            "Competitor Analysis": "",
            "Strategic Recommendations": "",
            "Appendices": ""
        }
        try:
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        except Exception as e:
            msg = f"Error loading summarization model: {e}"
            print(msg)
            self.logs.append(msg)
            self.summarizer = None

    def fetch_web_data(self, search_terms):
        example_urls = [
            "https://www.businessinsider.com/tesla-sales-slump-automakers-winning-gm-vw-byd-2025-4",
            "https://chargeasy.org/posts/the-ev-revolution-in-2025-a-comprehensive-look-at-market-trends-innovations-and-challenges"
        ]
        for url in example_urls:
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, "html.parser")
                paragraphs = [p.get_text() for p in soup.find_all("p")[:10]]
                self.sources.append("\n".join(paragraphs))
            except Exception as e:
                msg = f"Error fetching {url}: {e}"
                print(msg)
                self.logs.append(msg)

    def analyze_and_summarize(self):
        if not self.summarizer:
            return "Summarization model could not be loaded."

        combined_text = "\n\n".join(self.sources)
        truncated_text = combined_text[:4000]
        try:
            summary = self.summarizer(truncated_text, max_length=500, min_length=100, do_sample=False)[0]['summary_text']
        except Exception as e:
            msg = f"Error during summarization: {e}"
            print(msg)
            self.logs.append(msg)
            summary = "Summary could not be generated."
        return summary

    def fill_sections(self):
        summary = self.analyze_and_summarize()
        self.sections["Executive Summary"] = summary
        self.sections["Market Overview"] = "Global sales trends, regional insights, and forecasted EV adoption patterns."
        self.sections["Key Trends"] = "Solid-state batteries, fast-charging infrastructure, government incentives, EV policy shifts."
        self.sections["Competitor Analysis"] = "Competitive landscape including Tesla, GM, BYD, VW; analysis of market share and growth strategies."
        self.sections["Strategic Recommendations"] = "Expand into emerging markets, increase R&D in battery tech, form partnerships for charging networks, diversify supply chain sources."
        self.sections["Appendices"] = "Charts, graphs, external sources, and references supporting the data."

    def generate_report(self):
        self.fetch_web_data(self.query)
        self.fill_sections()

        report = f"# Electric Vehicle Market Intelligence Report\n\nGenerated on {datetime.now().strftime('%Y-%m-%d')}\n\n"
        for section, content in self.sections.items():
            report += f"## {section}\n{content}\n\n"
        return report, self.logs  # updated to return logs
