import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(text):
    # ★モデル名を指定せず「list_modelsで取得できるものを使う」
    models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]

    model_name = models[0]  # 一番使えるやつを自動選択
    model = genai.GenerativeModel(model_name)

    response = model.generate_content(text)
    return response.text