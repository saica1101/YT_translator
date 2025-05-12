import textwrap
import os
import google.generativeai as genai
from app.config import GEMINI_API_KEY

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY 環境変数が設定されていません")

genai.configure(api_key = api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

def summarize_in_english(text: str, chunk_size: int = 2000) -> str:
    if not text or text.strip() == "":
        return "No transcript available to summarize."
    
    chunks = textwrap.wrap(text, width=chunk_size)
    partial_summaries = []

    for chunk in chunks:
        prompt = f"Summarize the following transcript in 3-5 bullet points:\n\n{chunk}"
        response = model.generate_content(prompt)
        partial_summaries.append(response.parts[0].text.strip())

    final_prompt = "Based on the following bullet points, write a concise summary:\n\n" + "\n\n".join(partial_summaries)
    final_response = model.generate_content(final_prompt)

    return final_response.parts[0].text.strip()

def translate_to_japanese(summary: str) -> str:
    prompt = f"以下の英語の要約を自然な日本語に翻訳してください:\n\n{summary}"
    response = model.generate_content(prompt)
    return response.parts[0].text.strip()

def summarize_and_translate(text: str) -> str:
    english_summary = summarize_in_english(text)
    japanese_summary = translate_to_japanese(english_summary)
    return japanese_summary