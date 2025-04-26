# (BeautifulSoup + Requests + PDF Export with UTF-8 Fix)

import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
import os
import html

# custom EV article links
evs_urls = [
    "https://www.businessinsider.com/tesla-sales-slump-automakers-winning-gm-vw-byd-2025-4",
    "https://chargeasy.org/posts/the-ev-revolution-in-2025-a-comprehensive-look-at-market-trends-innovations-and-challenges"
]

def extract_article_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"url": url, "error": "Failed to fetch page"}

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract title
    title = soup.find("title").text.strip() if soup.find("title") else "No title found"

    # Extract publish date
    date = soup.find("time")
    date_text = date.get("datetime") if date else "No date found"

    # Extract main content
    paragraphs = soup.find_all("p")
    content = "\n".join([p.get_text(strip=True) for p in paragraphs])

    # Ensure the content is ASCII-friendly
    title = html.unescape(title).encode('latin-1', errors='replace').decode('latin-1')
    content = html.unescape(content).encode('latin-1', errors='replace').decode('latin-1')

    return {
        "url": url,
        "title": title,
        "date": date_text,
        "content": content[:5000]  # limit to first 5000 chars for LLM
    }

def scrape_all_ev_articles(urls):
    results = []
    for link in urls:
        print(f"Scraping: {link}")
        article = extract_article_data(link)
        results.append(article)
    return results

# Save articles to PDF
def save_articles_to_pdf(articles, filename="ev_articles.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for article in articles:
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 10, article['title'])
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 10, f"Date: {article['date']}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, article['content'])
        pdf.ln(10)

    pdf.output(filename)
    print(f"✅ PDF saved as {filename}")

# Example usage
if __name__ == "__main__":
    ev_articles = scrape_all_ev_articles(evs_urls)
    save_articles_to_pdf(ev_articles)
