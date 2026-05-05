import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.save import save_inquiry # 問い合わせを保存する関数
from backend.gemini import ask_gemini # Gemini APIを呼び出す関数

st.title("総務問い合わせ入力")
st.write("社員から総務への問い合わせを入力してください。")

# -------------------------
# 入力フォーム
# -------------------------
with st.form("inquiry_form"):
    name = st.text_input("氏名")
    category = st.selectbox("カテゴリ", ["休暇", "給与", "福利厚生", "その他"])
    priority = st.radio("緊急度", ["高", "中", "低"])
    question = st.text_area("問い合わせ内容", height=160)
    agree = st.checkbox("内容を確認しました")

    submitted = st.form_submit_button("送信する")

# -------------------------
# バリデーション & 表示
# -------------------------
if submitted:
    if not agree:
        st.error("内容確認にチェックしてください")
    elif question.strip() == "":
        st.error("問い合わせ内容を入力してください")
    else:
        st.success("登録が完了しました")

        st.subheader("Gemini回答")

        with st.spinner("AIが回答中..."):
            answer = ask_gemini(question)

        st.write(answer)

        st.subheader("入力内容")
        st.write("氏名:", name)
        st.write("カテゴリ:", category)
        st.write("緊急度:", priority)
        st.write("内容:", question)

# -------------------------
# メッセージ例（デモ）
# -------------------------
st.divider()

st.info("担当者が回答するまでお待ちください")
st.warning("この操作は取り消せません")
st.error("入力に誤りがあります")

# -------------------------
# サンプル一覧表示
# -------------------------
st.divider()
st.subheader("問い合わせ一覧（サンプル）")

inquiries = [
    {"id": 1, "question": "有給の申請方法は？", "category": "休暇"},
    {"id": 2, "question": "健康保険証を紛失した", "category": "その他"},
]

df = pd.DataFrame(inquiries)

st.dataframe(df)

# -------------------------
# レイアウト例
# -------------------------
col1, col2 = st.columns(2)

with col1:
    st.write("入力エリア")

with col2:
    st.write("回答エリア")

# -------------------------
# サイドバー
# -------------------------
st.sidebar.title("メニュー")
page = st.sidebar.radio("ページ", ["問い合わせ入力", "履歴一覧"])