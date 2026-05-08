import os
import re
import json
import httpx
# from urllib import response
# from google import genai
# from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from backend.storage import save_inquiry, load_inquiries

load_dotenv()

# Gemini_API_Key = os.getenv("Gemini_API_Key")
# client = genai.Client(api_key=Gemini_API_Key) # ① クライアント作成

# print("=== 利用可能なモデル一覧 ===")
# for model in genai.list_models():
#     if 'generateContent' in model.supported_generation_methods:
#         print(f"✅ {model.name}")
#     else:
#         print(f"❌ {model.name} (generateContentに対応していない)")

app = FastAPI()

# ── ① Gemini に返させる構造を定義 ──────────────────────────
class AnalysisResult(BaseModel):
    category: str   # 問い合わせカテゴリ
    priority: str   # 優先度
    answer: str     # 回答本文

# ── ② リクエストの形はそのまま ─────────────────────────────
class InquiryRequest(BaseModel):
    question: str  # 問い合わせ内容
    category: str
    priority: str
    name: str

PRIORITY_MAP = {"low": "低", "medium": "中", "high": "高"}

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):
    try:
        # ② プロンプト作成（指示文 + ユーザーの入力を埋め込む）
        # ── ③ プロンプトでカテゴリ・優先度・回答を指示 ────── #LLMに「JSON形式で返すように」と明示的に指示
        prompt = f"""
            以下の問い合わせを分析してください。
            必ずJSON形式のみで回答してください。
            説明文・マークダウン・コードブロックは一切不要です。
            最初の文字は必ず「{{」にしてください。

            問い合わせ: {request.question}
            入力カテゴリ: {request.category}
            入力優先度: {request.priority}

            返すJSONのキーは必ずこの3つにしてください:
            - "category" : 問い合わせの種類を日本語で（例: 休暇・給与・福利厚生・その他）
            - "priority"  : 緊急度を日本語で「高」「中」「低」のいずれかのみ
            - "answer"    : 問い合わせへの回答文（日本語・2〜3文程度）
            """
        # ── ④ response_mime_type で JSON を強制 ────────────
        # response = model.generate_content(
        #     prompt,
        #     generation_config=genai.GenerationConfig(
        #         response_mime_type="application/json",
        #         response_schema=AnalysisResult,   # Pydanticモデルをスキーマとして渡す
        #     )
        # )

        # 新SDKの書き方、③ LLMに送信・構造化出力で受け取る

        # response = client.models.generate_content(
        #     model="gemini-2.5-flash",
        #     contents=prompt,
        #     config=types.GenerateContentConfig(
        #         response_mime_type="application/json",
        #         response_schema=AnalysisResult,
        #     )
        # )

         # ✅ Ollama（ローカルLLM）
        response = httpx.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        raw = response.json()["response"]

        # JSONだけ抽出（余分なテキストを除去）
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError(f"JSONが見つかりませんでした: {raw}")

        category = result["category"]
        priority = PRIORITY_MAP.get(result["priority"], result["priority"])
        answer   = result["answer"]

        # print(response.text)
        # ── ⑤ JSONをパースして個別フィールドに分解 ──────────   # ④  一次回答の文章を作って結果をパースして使う
        # result = json.loads(response.text)
        # category = result["category"]
        # priority = PRIORITY_MAP.get(result["priority"], result["priority"])
        # answer   = result["answer"]

    except Exception as e:
        # エラー時はフォールバック値をセット
        category = request.category
        priority = request.priority
        answer = f"回答の取得に失敗しました: {str(e)}"

# ── ⑥ 個別フィールドをそのまま保存・返却 ────────────────
    item = save_inquiry(
        name=request.name,
        question=request.question,
        category=category,  # ← result["category"]
        priority=priority,  # ← result["priority"]
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