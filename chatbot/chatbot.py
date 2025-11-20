# Importing necessary libraries
import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

import google.generativeai as genai
import os
from dotenv import load_dotenv

index = faiss.read_index(r"C:\Users\laksh\Documents\LawLense Project\LawLense\vector_store\faiss_index.bin")
df = pd.read_csv(r"C:\Users\laksh\Documents\LawLense Project\LawLense\vector_store\article_lookup.csv")
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_articles(query, k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = []
    for idx in indices[0]:
        results.append({
            "title": df.iloc[idx]["title"],
            "content": df.iloc[idx]["content"]
        })
    
    return results

load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyD7cTB7J1xaLUTCD_GpZ-tgLhRl0mnyQ0Q"))
llm = genai.GenerativeModel("gemini-2.5-flash")

def answer_question(query, k=3):
    retrieved = retrieve_relevant_articles(query, k)
    
    # Build context for RAG
    context = "\n\n".join(
        [f"Article {r['title']}:\n{r['content']}" for r in retrieved]
    )

    prompt = f"""
    You are a legal expert chatbot for the Constitution of India.
    Use ONLY the context below to answer the user's question.

    Context:
    {context}

    Question:
    {query}

    Provide a helpful, accurate, and concise answer.
    """

    response = llm.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    question = "What does the right to life mean?"
    answer = answer_question(question)
    print(answer)
