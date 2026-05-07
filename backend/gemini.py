import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

def ask_gemini(text):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        return f"AIの回答取得に失敗しました: {e}"