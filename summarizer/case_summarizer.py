import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# ==============================
# 1. Initialize Gemini
# ==============================
genai.configure(api_key="AIzaSyD7cTB7J1xaLUTCD_GpZ-tgLhRl0mnyQ0Q")

model = genai.GenerativeModel("gemini-2.5-flash")

# ==============================
# 2. Fetch and extract text from the URL
# ==============================
def fetch_case_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract visible paragraph text
    paragraphs = soup.find_all("p")
    text = "\n".join(p.get_text() for p in paragraphs)

    # Limit to avoid model token overflow
    return text[:15000]


# ==============================
# 3. Summarize using Gemini
# ==============================
def summarize_case(text):
    prompt = f"""
    Summarize this court judgment in simple and clear language.
    Include:
    - What the case was about
    - Court's final decision
    - Key reasoning

    Text:
    {text}
    """

    result = model.generate_content(prompt)
    return result.text


# ==============================
# 4. Main Execution Flow
# ==============================
if __name__ == "__main__":
    url = input("Enter case URL: ")
    case_text = fetch_case_text(url)

    if case_text.strip():
        summary = summarize_case(case_text)
        print("\n================= SUMMARY =================\n")
        print(summary)
    else:
        print("❌ Could not extract readable content from the page.")
