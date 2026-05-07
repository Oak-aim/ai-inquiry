import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.storage import save_inquiry, load_inquiries

load_dotenv()

Gemini_API_Key = os.getenv("Gemini_API_Key")
genai.configure(api_key=Gemini_API_Key)

# print("=== 利用可能なモデル一覧 ===")
# for model in genai.list_models():
#     if 'generateContent' in model.supported_generation_methods:
#         print(f"✅ {model.name}")
#     else:
#         print(f"❌ {model.name} (generateContentに対応していない)")

app = FastAPI()

class InquiryRequest(BaseModel):
    question: str  # 問い合わせ内容
    category: str
    priority: str
    name: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):
    try:
        # タイムアウト設定と詳細エラー表示
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(request.question)
        answer = response.text
    except Exception as e:
        answer = f"回答の取得に失敗しました: {str(e)}"

    item = save_inquiry(  
        name=request.name,        # ← ミニ課題2の return {...} からsave_inquiryを呼ぶように書き換える
        question=request.question,
        category=request.category,
        priority=request.priority,
        answer=answer
    )
    return item

    # return {
    #     "category": request.category, #requestからカテゴリをそのまま返す
    #     "priority": request.priority,
    #     "answer": answer
    # }

@app.get("/inquiries")
def get_inquiries():
    return load_inquiries()